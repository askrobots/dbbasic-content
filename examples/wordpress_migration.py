"""
WordPress migration example.

Shows how to import content from WordPress database.
"""

from dbbasic_content import WordPressImporter, ContentDB

# Import from WordPress database
with WordPressImporter(
    host='localhost',
    database='wordpress',
    user='root',
    password='secret'
) as importer:
    # Import all content
    stats = importer.import_to('/var/app/content')

    print("Import complete!")
    print(f"  Posts: {stats['posts']}")
    print(f"  Pages: {stats['pages']}")
    print(f"  Drafts: {stats['drafts']}")
    print(f"  Total: {sum(stats.values())}")

# Verify imported content
content = ContentDB('/var/app/content')
posts = content.get_posts()

print(f"\nVerification: Found {len(posts)} posts in content directory")

# Show sample post
if posts:
    sample = posts[0]
    print(f"\nSample post:")
    print(f"  Slug: {sample['slug']}")
    print(f"  Title: {sample['title']}")
    print(f"  Blocks: {len(sample['blocks'])}")

# Show categories and tags
categories = content.get_categories()
tags = content.get_tags()

print(f"\nCategories: {', '.join(categories)}")
print(f"Tags: {', '.join(tags[:10])}..." if len(tags) > 10 else f"Tags: {', '.join(tags)}")
