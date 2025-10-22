#!/usr/bin/env python3
"""
Example demonstrating posts vs pages in dbbasic-content.

This shows how to use dbbasic-content for a site with both:
- Blog posts (dated, categorized)
- Static pages (documentation, about, etc.)
"""

import tempfile
from pathlib import Path
from dbbasic_content import ContentDB


def main():
    # Create a temporary content directory for this example
    with tempfile.TemporaryDirectory() as tmpdir:
        content = ContentDB(tmpdir)

        print("=" * 60)
        print("dbbasic-content: Posts vs Pages Example")
        print("=" * 60)
        print()

        # Create some blog posts
        print("Creating blog posts...")
        content.create_post(
            slug='announcing-v1',
            title='Announcing Version 1.0',
            content_type='post',
            date='2025-10-20',
            author='admin',
            categories=['Announcements', 'Releases'],
            tags=['v1', 'release'],
            blocks=[
                {'type': 'heading', 'data': {'level': 1, 'content': 'Announcing Version 1.0'}},
                {'type': 'paragraph', 'data': {'content': 'We are excited to announce version 1.0!'}},
            ]
        )

        content.create_post(
            slug='getting-started',
            title='Getting Started with DBBasic',
            content_type='post',
            date='2025-10-21',
            author='admin',
            categories=['Tutorials'],
            tags=['tutorial', 'beginner'],
            blocks=[
                {'type': 'heading', 'data': {'level': 1, 'content': 'Getting Started'}},
                {'type': 'paragraph', 'data': {'content': 'This tutorial will help you get started...'}},
            ]
        )

        # Create some static pages
        print("Creating static pages...")
        content.create_page(
            slug='about',
            title='About DBBasic',
            blocks=[
                {'type': 'heading', 'data': {'level': 1, 'content': 'About DBBasic'}},
                {'type': 'paragraph', 'data': {'content': 'DBBasic is a Unix-foundation content management system.'}},
            ]
        )

        content.create_page(
            slug='api-docs',
            title='API Documentation',
            blocks=[
                {'type': 'heading', 'data': {'level': 1, 'content': 'API Documentation'}},
                {'type': 'paragraph', 'data': {'content': 'Complete API reference for DBBasic.'}},
                {'type': 'code', 'data': {'code': 'from dbbasic_content import ContentDB', 'language': 'python'}},
            ]
        )

        content.create_page(
            slug='contact',
            title='Contact Us',
            blocks=[
                {'type': 'heading', 'data': {'level': 1, 'content': 'Contact Us'}},
                {'type': 'paragraph', 'data': {'content': 'Get in touch: hello@example.com'}},
            ]
        )

        print()
        print("-" * 60)
        print("Directory Structure:")
        print("-" * 60)

        # Show directory structure
        for subdir in ['posts', 'pages', 'articles']:
            dir_path = Path(tmpdir) / subdir
            if dir_path.exists():
                files = list(dir_path.glob('*.json'))
                print(f"{subdir}/")
                for f in files:
                    print(f"  - {f.name}")

        print()
        print("-" * 60)
        print("Blog Posts (chronological):")
        print("-" * 60)

        # Get all posts
        posts = content.get_posts(content_type='post', order_by='date', order='desc')
        for post in posts:
            print(f"  [{post['date']}] {post['title']}")
            print(f"    Categories: {', '.join(post.get('categories', []))}")
            print(f"    Tags: {', '.join(post.get('tags', []))}")
            print()

        print("-" * 60)
        print("Static Pages (alphabetical):")
        print("-" * 60)

        # Get all pages
        pages = content.get_pages(order_by='title', order='asc')
        for page in pages:
            print(f"  {page['title']}")
            print(f"    Slug: {page['slug']}")
            print(f"    Type: {page['content_type']}")
            print()

        print("-" * 60)
        print("Example Queries:")
        print("-" * 60)

        # Query examples
        print("\n1. Get posts in 'Tutorials' category:")
        tutorial_posts = content.get_posts(content_type='post', categories=['Tutorials'])
        for post in tutorial_posts:
            print(f"   - {post['title']}")

        print("\n2. Get specific page:")
        about = content.get_page('about')
        print(f"   Title: {about['title']}")
        print(f"   Type: {about['content_type']}")

        print("\n3. Check if content exists:")
        print(f"   Post 'announcing-v1' exists: {content.post_exists('announcing-v1', content_type='post')}")
        print(f"   Page 'about' exists: {content.page_exists('about')}")
        print(f"   Page 'nonexistent' exists: {content.page_exists('nonexistent')}")

        print()
        print("=" * 60)
        print("Key Differences:")
        print("=" * 60)
        print("Posts:  Have dates, categories, tags - for blog content")
        print("Pages:  No dates/categories/tags - for static content")
        print("Both:   Use the same block-based format")
        print("=" * 60)


if __name__ == '__main__':
    main()
