"""
ContentDB: WordPress-like API for block-based JSON content

Provides familiar WordPress methods (get_post, get_posts) but backed by
filesystem JSON files instead of MySQL.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ContentDB:
    """
    Content database backed by JSON files on disk.

    Unix Gateway Pattern: Thin layer over filesystem primitives.

    Storage structure:
        /content/
            articles/
                hello-world.json
                about.json
            metadata.tsv
            taxonomy.tsv
    """

    def __init__(self, content_dir: str):
        """
        Initialize ContentDB.

        Args:
            content_dir: Path to content directory
        """
        self.content_dir = Path(content_dir)
        self.articles_dir = self.content_dir / "articles"

        # Create directories if they don't exist
        self.articles_dir.mkdir(parents=True, exist_ok=True)

    def get_post(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Get a single post by slug (like WordPress get_post).

        Args:
            slug: Post slug

        Returns:
            Post data dict or None if not found
        """
        article_path = self.articles_dir / f"{slug}.json"

        if not article_path.exists():
            return None

        with open(article_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_posts(
        self,
        status: Optional[str] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
        order_by: str = 'date',
        order: str = 'desc'
    ) -> List[Dict[str, Any]]:
        """
        Get multiple posts with filtering (like WordPress WP_Query).

        Args:
            status: Filter by status (published, draft, etc.)
            categories: Filter by categories
            tags: Filter by tags
            author: Filter by author
            limit: Maximum number of posts to return
            offset: Number of posts to skip
            order_by: Field to order by (date, title, etc.)
            order: Order direction (asc or desc)

        Returns:
            List of post dicts
        """
        posts = []

        # Read all JSON files from articles directory
        for article_path in self.articles_dir.glob("*.json"):
            try:
                with open(article_path, 'r', encoding='utf-8') as f:
                    post = json.load(f)
                    posts.append(post)
            except (json.JSONDecodeError, IOError):
                # Skip invalid files
                continue

        # Filter by status
        if status:
            posts = [p for p in posts if p.get('status') == status]

        # Filter by categories
        if categories:
            posts = [
                p for p in posts
                if any(cat in p.get('categories', []) for cat in categories)
            ]

        # Filter by tags
        if tags:
            posts = [
                p for p in posts
                if any(tag in p.get('tags', []) for tag in tags)
            ]

        # Filter by author
        if author:
            posts = [p for p in posts if p.get('author') == author]

        # Sort posts
        reverse = (order == 'desc')
        try:
            posts.sort(key=lambda p: p.get(order_by, ''), reverse=reverse)
        except TypeError:
            # If comparison fails, skip sorting
            pass

        # Apply offset and limit
        if offset:
            posts = posts[offset:]
        if limit:
            posts = posts[:limit]

        return posts

    def create_post(
        self,
        slug: str,
        title: str,
        blocks: List[Dict[str, Any]],
        author: str = "admin",
        date: Optional[str] = None,
        status: str = "published",
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new post (like WordPress wp_insert_post).

        Args:
            slug: URL slug
            title: Post title
            blocks: List of content blocks
            author: Post author
            date: Publication date (ISO format, defaults to now)
            status: Post status (published, draft, etc.)
            categories: List of categories
            tags: List of tags
            description: Meta description
            **kwargs: Additional metadata

        Returns:
            Created post data
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        post = {
            "slug": slug,
            "title": title,
            "date": date,
            "author": author,
            "status": status,
            "blocks": blocks,
        }

        if categories:
            post["categories"] = categories
        if tags:
            post["tags"] = tags
        if description:
            post["description"] = description

        # Add any additional metadata
        post.update(kwargs)

        # Write to file
        article_path = self.articles_dir / f"{slug}.json"
        with open(article_path, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)

        return post

    def update_post(self, slug: str, **updates) -> Optional[Dict[str, Any]]:
        """
        Update an existing post (like WordPress wp_update_post).

        Args:
            slug: Post slug
            **updates: Fields to update

        Returns:
            Updated post data or None if not found
        """
        post = self.get_post(slug)
        if not post:
            return None

        # Update fields
        post.update(updates)

        # Write back to file
        article_path = self.articles_dir / f"{slug}.json"
        with open(article_path, 'w', encoding='utf-8') as f:
            json.dump(post, f, indent=2, ensure_ascii=False)

        return post

    def delete_post(self, slug: str) -> bool:
        """
        Delete a post (like WordPress wp_delete_post).

        Args:
            slug: Post slug

        Returns:
            True if deleted, False if not found
        """
        article_path = self.articles_dir / f"{slug}.json"

        if not article_path.exists():
            return False

        article_path.unlink()
        return True

    def post_exists(self, slug: str) -> bool:
        """
        Check if a post exists.

        Args:
            slug: Post slug

        Returns:
            True if exists, False otherwise
        """
        article_path = self.articles_dir / f"{slug}.json"
        return article_path.exists()

    def get_categories(self) -> List[str]:
        """
        Get all unique categories across all posts.

        Returns:
            List of category names
        """
        categories = set()
        for post in self.get_posts():
            categories.update(post.get('categories', []))
        return sorted(list(categories))

    def get_tags(self) -> List[str]:
        """
        Get all unique tags across all posts.

        Returns:
            List of tag names
        """
        tags = set()
        for post in self.get_posts():
            tags.update(post.get('tags', []))
        return sorted(list(tags))

    def get_authors(self) -> List[str]:
        """
        Get all unique authors across all posts.

        Returns:
            List of author names
        """
        authors = set()
        for post in self.get_posts():
            if 'author' in post:
                authors.add(post['author'])
        return sorted(list(authors))

    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Simple text search across posts (title, description, block content).

        Args:
            query: Search query string

        Returns:
            List of matching posts
        """
        query_lower = query.lower()
        results = []

        for post in self.get_posts():
            # Check title
            if query_lower in post.get('title', '').lower():
                results.append(post)
                continue

            # Check description
            if query_lower in post.get('description', '').lower():
                results.append(post)
                continue

            # Check block content
            for block in post.get('blocks', []):
                block_data = json.dumps(block.get('data', {})).lower()
                if query_lower in block_data:
                    results.append(post)
                    break

        return results
