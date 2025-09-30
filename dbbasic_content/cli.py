"""
CLI tools for dbbasic-content.

Unix-style command-line interface for content management.
"""

import sys
import argparse
from pathlib import Path
from .content import ContentDB
from .wordpress_importer import WordPressImporter
from .blocks import validate_blocks


def cmd_init(args):
    """Initialize a new content directory."""
    content_path = Path(args.path)

    if content_path.exists() and any(content_path.iterdir()):
        print(f"Error: Directory {args.path} already exists and is not empty", file=sys.stderr)
        return 1

    # Create ContentDB (will create directories)
    ContentDB(args.path)

    print(f"Initialized content directory at {args.path}")
    print(f"  articles/  - Article JSON files")

    return 0


def cmd_list(args):
    """List all posts."""
    db = ContentDB(args.path)
    posts = db.get_posts()

    if not posts:
        print("No posts found")
        return 0

    # Display posts
    for post in posts:
        status = post.get('status', 'unknown')
        date = post.get('date', 'no-date')
        title = post.get('title', 'Untitled')
        slug = post.get('slug', 'no-slug')

        print(f"{slug:30} {date:12} {status:10} {title}")

    print(f"\nTotal: {len(posts)} posts")
    return 0


def cmd_show(args):
    """Show post details."""
    db = ContentDB(args.path)
    post = db.get_post(args.slug)

    if not post:
        print(f"Error: Post '{args.slug}' not found", file=sys.stderr)
        return 1

    # Display post details
    print(f"Slug: {post.get('slug')}")
    print(f"Title: {post.get('title')}")
    print(f"Date: {post.get('date')}")
    print(f"Author: {post.get('author')}")
    print(f"Status: {post.get('status', 'published')}")

    if 'categories' in post:
        print(f"Categories: {', '.join(post['categories'])}")

    if 'tags' in post:
        print(f"Tags: {', '.join(post['tags'])}")

    if 'description' in post:
        print(f"\nDescription:\n{post['description']}")

    blocks = post.get('blocks', [])
    print(f"\nBlocks: {len(blocks)}")
    for i, block in enumerate(blocks):
        print(f"  {i+1}. {block['type']}")

    return 0


def cmd_validate(args):
    """Validate content structure."""
    db = ContentDB(args.path)
    posts = db.get_posts()

    if not posts:
        print("No posts to validate")
        return 0

    errors = []

    for post in posts:
        slug = post.get('slug', 'unknown')

        # Validate required fields
        required = ['slug', 'title', 'blocks']
        for field in required:
            if field not in post:
                errors.append(f"{slug}: Missing required field '{field}'")

        # Validate blocks
        blocks = post.get('blocks', [])
        is_valid, block_errors = validate_blocks(blocks)
        if not is_valid:
            for error in block_errors:
                errors.append(f"{slug}: {error}")

    if errors:
        print(f"Validation failed with {len(errors)} errors:\n")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Validation passed for {len(posts)} posts")
    return 0


def cmd_import_wordpress(args):
    """Import from WordPress database."""
    print(f"Importing from WordPress database...")
    print(f"  Host: {args.host}")
    print(f"  Database: {args.database}")
    print(f"  Output: {args.path}")
    print()

    try:
        with WordPressImporter(
            host=args.host,
            database=args.database,
            user=args.user,
            password=args.password,
            port=args.port,
            table_prefix=args.prefix
        ) as importer:
            stats = importer.import_to(args.path)

            print("Import complete:")
            print(f"  Posts: {stats['posts']}")
            print(f"  Pages: {stats['pages']}")
            print(f"  Drafts: {stats['drafts']}")
            print(f"  Total: {sum(stats.values())}")

        return 0

    except ImportError:
        print("Error: pymysql not installed", file=sys.stderr)
        print("Install with: pip install dbbasic-content[wordpress]", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_categories(args):
    """List all categories."""
    db = ContentDB(args.path)
    categories = db.get_categories()

    if not categories:
        print("No categories found")
        return 0

    for category in categories:
        # Count posts in category
        posts = db.get_posts(categories=[category])
        print(f"{category:30} ({len(posts)} posts)")

    return 0


def cmd_tags(args):
    """List all tags."""
    db = ContentDB(args.path)
    tags = db.get_tags()

    if not tags:
        print("No tags found")
        return 0

    for tag in tags:
        # Count posts with tag
        posts = db.get_posts(tags=[tag])
        print(f"{tag:30} ({len(posts)} posts)")

    return 0


def cmd_search(args):
    """Search posts."""
    db = ContentDB(args.path)
    results = db.search(args.query)

    if not results:
        print(f"No results found for: {args.query}")
        return 0

    print(f"Found {len(results)} results for: {args.query}\n")

    for post in results:
        slug = post.get('slug', 'no-slug')
        title = post.get('title', 'Untitled')
        print(f"  {slug:30} {title}")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='dbbasic-content: Unix-foundation content management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize new content directory
  dbcontent init /var/app/content

  # List all posts
  dbcontent list /var/app/content

  # Show post details
  dbcontent show /var/app/content hello-world

  # Import from WordPress
  dbcontent import wordpress \\
    --host localhost \\
    --database wordpress \\
    --user root \\
    --password secret \\
    /var/app/content

  # Validate content
  dbcontent validate /var/app/content

  # Search posts
  dbcontent search /var/app/content "python programming"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # init command
    parser_init = subparsers.add_parser('init', help='Initialize content directory')
    parser_init.add_argument('path', help='Path to content directory')

    # list command
    parser_list = subparsers.add_parser('list', help='List all posts')
    parser_list.add_argument('path', help='Path to content directory')

    # show command
    parser_show = subparsers.add_parser('show', help='Show post details')
    parser_show.add_argument('path', help='Path to content directory')
    parser_show.add_argument('slug', help='Post slug')

    # validate command
    parser_validate = subparsers.add_parser('validate', help='Validate content structure')
    parser_validate.add_argument('path', help='Path to content directory')

    # import wordpress command
    parser_import = subparsers.add_parser('import', help='Import from WordPress')
    import_subparsers = parser_import.add_subparsers(dest='import_type', help='Import type')

    parser_wp = import_subparsers.add_parser('wordpress', help='Import from WordPress database')
    parser_wp.add_argument('path', help='Path to content directory')
    parser_wp.add_argument('--host', default='localhost', help='MySQL host')
    parser_wp.add_argument('--database', required=True, help='Database name')
    parser_wp.add_argument('--user', required=True, help='MySQL user')
    parser_wp.add_argument('--password', required=True, help='MySQL password')
    parser_wp.add_argument('--port', type=int, default=3306, help='MySQL port')
    parser_wp.add_argument('--prefix', default='wp_', help='Table prefix')

    # categories command
    parser_categories = subparsers.add_parser('categories', help='List all categories')
    parser_categories.add_argument('path', help='Path to content directory')

    # tags command
    parser_tags = subparsers.add_parser('tags', help='List all tags')
    parser_tags.add_argument('path', help='Path to content directory')

    # search command
    parser_search = subparsers.add_parser('search', help='Search posts')
    parser_search.add_argument('path', help='Path to content directory')
    parser_search.add_argument('query', help='Search query')

    # Parse args
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to command handlers
    commands = {
        'init': cmd_init,
        'list': cmd_list,
        'show': cmd_show,
        'validate': cmd_validate,
        'categories': cmd_categories,
        'tags': cmd_tags,
        'search': cmd_search,
    }

    if args.command == 'import' and args.import_type == 'wordpress':
        return cmd_import_wordpress(args)

    if args.command in commands:
        return commands[args.command](args)

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
