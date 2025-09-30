"""
WordPress importer: Convert wp_posts to JSON blocks.

Extracts content from WordPress MySQL database and converts to
block-based JSON format.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from html.parser import HTMLParser


class HTMLToBlocksParser(HTMLParser):
    """
    Parse WordPress HTML content into blocks.

    WordPress stores content as HTML. We need to extract it into
    structured blocks.
    """

    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_tag = None
        self.current_data = []
        self.list_items = []
        self.in_list = False

    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        self.current_tag = tag

        if tag in ['ul', 'ol']:
            self.in_list = True
            self.list_type = 'unordered' if tag == 'ul' else 'ordered'
            self.list_items = []

    def handle_endtag(self, tag):
        """Handle closing HTML tags."""
        if tag == 'p' and self.current_data:
            content = ''.join(self.current_data).strip()
            if content:
                self.blocks.append({
                    'type': 'paragraph',
                    'data': {'content': content}
                })
            self.current_data = []

        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.current_data:
            level = int(tag[1])
            content = ''.join(self.current_data).strip()
            if content:
                self.blocks.append({
                    'type': 'heading',
                    'data': {'level': level, 'content': content}
                })
            self.current_data = []

        elif tag == 'li' and self.current_data:
            content = ''.join(self.current_data).strip()
            if content:
                self.list_items.append(content)
            self.current_data = []

        elif tag in ['ul', 'ol']:
            if self.list_items:
                self.blocks.append({
                    'type': 'list',
                    'data': {
                        'listType': self.list_type,
                        'items': self.list_items
                    }
                })
            self.list_items = []
            self.in_list = False

        elif tag == 'blockquote' and self.current_data:
            content = ''.join(self.current_data).strip()
            if content:
                self.blocks.append({
                    'type': 'quote',
                    'data': {'content': content}
                })
            self.current_data = []

        elif tag == 'pre' and self.current_data:
            code = ''.join(self.current_data).strip()
            if code:
                self.blocks.append({
                    'type': 'code',
                    'data': {'code': code, 'language': 'text'}
                })
            self.current_data = []

        self.current_tag = None

    def handle_data(self, data):
        """Handle text data between tags."""
        if self.current_tag:
            self.current_data.append(data)
        else:
            # Text outside tags - treat as paragraph
            data = data.strip()
            if data:
                self.current_data.append(data)

    def get_blocks(self) -> List[Dict[str, Any]]:
        """Get parsed blocks."""
        # Handle any remaining data
        if self.current_data and not self.in_list:
            content = ''.join(self.current_data).strip()
            if content:
                self.blocks.append({
                    'type': 'paragraph',
                    'data': {'content': content}
                })

        return self.blocks


class WordPressImporter:
    """
    Import WordPress content to JSON block format.

    Connects to WordPress MySQL database and extracts posts,
    converting them to our block-based JSON format.
    """

    def __init__(
        self,
        host: str = "localhost",
        database: str = "wordpress",
        user: str = "root",
        password: str = "",
        port: int = 3306,
        table_prefix: str = "wp_"
    ):
        """
        Initialize WordPress importer.

        Args:
            host: MySQL host
            database: Database name
            user: MySQL user
            password: MySQL password
            port: MySQL port
            table_prefix: WordPress table prefix (default: wp_)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.table_prefix = table_prefix
        self._connection = None

    def _connect(self):
        """Connect to MySQL database (lazy)."""
        if self._connection is None:
            try:
                import pymysql
            except ImportError:
                raise ImportError(
                    "pymysql required for WordPress import. "
                    "Install with: pip install dbbasic-content[wordpress]"
                )

            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        return self._connection

    def _get_posts(self, post_type: str = 'post') -> List[Dict[str, Any]]:
        """
        Get posts from WordPress database.

        Args:
            post_type: WordPress post type (post, page, etc.)

        Returns:
            List of post dicts
        """
        conn = self._connect()
        with conn.cursor() as cursor:
            query = f"""
                SELECT
                    ID,
                    post_title,
                    post_name,
                    post_content,
                    post_excerpt,
                    post_status,
                    post_date,
                    post_author
                FROM {self.table_prefix}posts
                WHERE post_type = %s
                AND post_status IN ('publish', 'draft')
                ORDER BY post_date DESC
            """
            cursor.execute(query, (post_type,))
            return cursor.fetchall()

    def _get_post_meta(self, post_id: int) -> Dict[str, Any]:
        """Get post metadata."""
        conn = self._connect()
        meta = {}
        with conn.cursor() as cursor:
            query = f"""
                SELECT meta_key, meta_value
                FROM {self.table_prefix}postmeta
                WHERE post_id = %s
            """
            cursor.execute(query, (post_id,))
            for row in cursor.fetchall():
                meta[row['meta_key']] = row['meta_value']
        return meta

    def _get_terms(self, post_id: int, taxonomy: str) -> List[str]:
        """Get post terms (categories, tags)."""
        conn = self._connect()
        terms = []
        with conn.cursor() as cursor:
            query = f"""
                SELECT t.name
                FROM {self.table_prefix}terms t
                JOIN {self.table_prefix}term_taxonomy tt ON t.term_id = tt.term_id
                JOIN {self.table_prefix}term_relationships tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
                WHERE tr.object_id = %s
                AND tt.taxonomy = %s
            """
            cursor.execute(query, (post_id, taxonomy))
            terms = [row['name'] for row in cursor.fetchall()]
        return terms

    def _convert_content_to_blocks(self, content: str) -> List[Dict[str, Any]]:
        """
        Convert WordPress HTML content to blocks.

        Args:
            content: WordPress post_content HTML

        Returns:
            List of blocks
        """
        if not content or not content.strip():
            return []

        # Parse HTML into blocks
        parser = HTMLToBlocksParser()
        parser.feed(content)
        blocks = parser.get_blocks()

        # If no blocks parsed, treat entire content as single paragraph
        if not blocks:
            blocks = [{
                'type': 'paragraph',
                'data': {'content': content.strip()}
            }]

        return blocks

    def import_posts(
        self,
        output_dir: str,
        post_type: str = 'post',
        status_filter: Optional[List[str]] = None
    ) -> int:
        """
        Import WordPress posts to JSON files.

        Args:
            output_dir: Directory to write JSON files
            post_type: WordPress post type to import
            status_filter: Filter by post status (None = all)

        Returns:
            Number of posts imported
        """
        output_path = Path(output_dir)
        articles_dir = output_path / "articles"
        articles_dir.mkdir(parents=True, exist_ok=True)

        posts = self._get_posts(post_type)
        imported_count = 0

        for wp_post in posts:
            # Filter by status if specified
            if status_filter and wp_post['post_status'] not in status_filter:
                continue

            # Get additional data
            categories = self._get_terms(wp_post['ID'], 'category')
            tags = self._get_terms(wp_post['ID'], 'post_tag')
            meta = self._get_post_meta(wp_post['ID'])

            # Convert content to blocks
            blocks = self._convert_content_to_blocks(wp_post['post_content'])

            # Build article JSON
            article = {
                'slug': wp_post['post_name'] or f"post-{wp_post['ID']}",
                'title': wp_post['post_title'],
                'date': wp_post['post_date'].strftime('%Y-%m-%d'),
                'author': str(wp_post['post_author']),
                'status': wp_post['post_status'],
                'blocks': blocks,
            }

            if wp_post['post_excerpt']:
                article['description'] = wp_post['post_excerpt']

            if categories:
                article['categories'] = categories

            if tags:
                article['tags'] = tags

            # Add WordPress ID for reference
            article['wordpress_id'] = wp_post['ID']

            # Write to file
            filename = f"{article['slug']}.json"
            filepath = articles_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(article, f, indent=2, ensure_ascii=False)

            imported_count += 1

        return imported_count

    def import_to(self, output_dir: str) -> Dict[str, int]:
        """
        Import all WordPress content to directory.

        Args:
            output_dir: Directory to write content

        Returns:
            Dict with counts of imported items
        """
        stats = {
            'posts': self.import_posts(output_dir, post_type='post', status_filter=['publish']),
            'pages': self.import_posts(output_dir, post_type='page', status_filter=['publish']),
            'drafts': self.import_posts(output_dir, post_type='post', status_filter=['draft']),
        }

        return stats

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        """Context manager support."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
