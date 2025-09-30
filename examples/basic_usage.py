"""
Basic usage examples for dbbasic-content.
"""

from dbbasic_content import ContentDB

# Initialize content database
content = ContentDB('/tmp/example_content')

# Create a post
post = content.create_post(
    slug='hello-world',
    title='Hello World',
    author='john',
    categories=['Technology', 'Python'],
    tags=['tutorial', 'beginner'],
    blocks=[
        {
            'type': 'paragraph',
            'data': {
                'content': 'Welcome to my blog! This is my first post.'
            }
        },
        {
            'type': 'heading',
            'data': {
                'level': 2,
                'content': 'Getting Started'
            }
        },
        {
            'type': 'paragraph',
            'data': {
                'content': 'Here are some things you should know...'
            }
        },
        {
            'type': 'list',
            'data': {
                'listType': 'unordered',
                'items': [
                    'Item one',
                    'Item two',
                    'Item three'
                ]
            }
        }
    ]
)

print(f"Created post: {post['slug']}")

# Get a post
retrieved_post = content.get_post('hello-world')
print(f"Retrieved: {retrieved_post['title']}")

# Get all published posts
posts = content.get_posts(status='published', limit=10)
print(f"Found {len(posts)} published posts")

# Get posts by category
tech_posts = content.get_posts(categories=['Technology'])
print(f"Found {len(tech_posts)} tech posts")

# Search posts
results = content.search('Python')
print(f"Search found {len(results)} results")

# Update a post
updated = content.update_post(
    'hello-world',
    title='Hello World - Updated!',
    status='draft'
)
print(f"Updated post: {updated['title']}")

# Get all categories
categories = content.get_categories()
print(f"Categories: {', '.join(categories)}")

# Get all tags
tags = content.get_tags()
print(f"Tags: {', '.join(tags)}")
