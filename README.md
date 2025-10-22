# dbbasic-content

[![PyPI version](https://badge.fury.io/py/dbbasic-content.svg)](https://pypi.org/project/dbbasic-content/)
[![Python versions](https://img.shields.io/pypi/pyversions/dbbasic-content.svg)](https://pypi.org/project/dbbasic-content/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Unix-foundation content management for web apps**

Part of the WordPress escape toolkit. Build on Unix foundations instead of rebuilding everything badly.

## Philosophy

> "Web development takes forever because we reject the solid foundation and build on sand."

dbbasic-content provides WordPress-like content management built on Unix principles:
- Content stored as **JSON files** on disk (not MySQL)
- Block-based structure (like Gutenberg)
- Simple filesystem operations (grep, cat, version control)
- Zero database daemon required
- Deploy with rsync/FTP like it's 1995 (but better)

## Features

- **ContentDB**: WordPress-like API (`get_post`, `get_posts`, `get_page`, `get_pages`)
- **Posts vs Pages**: Separate blog posts (dated, categorized) from static pages
- **Block-based**: Paragraph, heading, list, card, code, and more
- **WordPress Import**: Migrate from wp_posts to JSON blocks
- **Unix Gateway**: Thin layer over filesystem primitives
- **Version Control Friendly**: JSON files in git
- **Grep-able**: Find content with standard Unix tools
- **Backward Compatible**: Existing `articles/` directory still works

## Installation

```bash
# From PyPI
pip install dbbasic-content

# With WordPress import support
pip install dbbasic-content[wordpress]

# From source (development)
pip install git+https://github.com/askrobots/dbbasic-content.git
```

## Quick Start

### Posts (Blog Articles)

```python
from dbbasic_content import ContentDB

# Initialize content database
content = ContentDB('/var/app/content')

# Get a post by slug
post = content.get_post('hello-world', content_type='post')

# Get published posts
posts = content.get_posts(content_type='post', status='published', limit=10)

# Get posts by category
tech_posts = content.get_posts(content_type='post', categories=['Technology'])

# Add a new post
content.create_post(
    slug='new-post',
    title='My New Post',
    content_type='post',
    author='john',
    blocks=[
        {'type': 'paragraph', 'data': {'content': 'Hello world!'}},
        {'type': 'heading', 'data': {'level': 2, 'content': 'Subheading'}},
    ]
)
```

### Pages (Static Content)

```python
# Create a page (no date, categories, or tags)
content.create_page(
    slug='about',
    title='About Us',
    blocks=[
        {'type': 'heading', 'data': {'level': 1, 'content': 'About Us'}},
        {'type': 'paragraph', 'data': {'content': 'We are building the future...'}},
    ]
)

# Get a page
about = content.get_page('about')

# Get all pages
pages = content.get_pages(status='published')

# Update a page
content.update_page('about', title='About Our Company')

# Delete a page
content.delete_page('old-page')
```

### Posts vs Pages: What's the Difference?

Following WordPress conventions:

**Posts (Blog Articles)**
- Have publication dates
- Support categories and tags
- Displayed chronologically (newest first)
- Appear in RSS feeds
- Used for: Blog posts, news articles, announcements

**Pages (Static Content)**
- No dates (timeless content)
- No categories or tags
- Displayed alphabetically or by menu order
- Don't appear in RSS feeds
- Used for: About, Contact, Documentation, Specs

```python
# Create a blog post
content.create_post(
    slug='announcing-v2',
    title='Announcing Version 2.0',
    content_type='post',
    date='2025-10-22',
    categories=['Announcements'],
    blocks=[...]
)

# Create a documentation page
content.create_page(
    slug='api-docs',
    title='API Documentation',
    blocks=[...]  # No date, no categories
)
```

## WordPress Migration

```python
from dbbasic_content import WordPressImporter

# Import from WordPress database
importer = WordPressImporter(
    host='localhost',
    database='wordpress',
    user='root',
    password='secret'
)

# Convert to JSON blocks
importer.import_to('/var/app/content')

# Converts:
# - wp_posts → articles/*.json
# - wp_postmeta → block metadata
# - wp_terms → categories/tags
# - wp_comments → comments.tsv
```

## CLI Tools

```bash
# Initialize content directory
dbcontent init /var/app/content

# Import from WordPress
dbcontent import wordpress \
  --host localhost \
  --database wordpress \
  --user root \
  --password secret \
  /var/app/content

# List all posts
dbcontent list /var/app/content

# Get post details
dbcontent show /var/app/content hello-world

# Validate content structure
dbcontent validate /var/app/content
```

## Block Types

Supported block types (like Gutenberg):

- `paragraph` - Rich text content
- `heading` - Headings (h1-h6)
- `list` - Ordered/unordered lists
- `card` - Styled content boxes
- `card_list` - Multiple cards
- `code` - Syntax-highlighted code
- `image` - Images with captions
- `quote` - Blockquotes

Extensible - add your own block types.

## Storage Format

```
/var/app/content/
├── articles/          # Legacy (backward compatible)
│   └── old-post.json
├── posts/             # Blog posts (dated, categorized)
│   ├── hello-world.json
│   └── tech-post.json
├── pages/             # Static pages (no date/categories)
│   ├── about.json
│   └── contact.json
├── metadata.tsv       # Post metadata (searchable)
├── taxonomy.tsv       # Categories/tags
└── comments.tsv       # Comments (if enabled)
```

### Post Format (Blog Article)

```json
{
  "slug": "hello-world",
  "title": "Hello World",
  "content_type": "post",
  "date": "2025-01-15",
  "author": "john",
  "categories": ["Technology"],
  "tags": ["python", "web"],
  "blocks": [
    {
      "type": "paragraph",
      "data": {"content": "Hello world!"}
    }
  ]
}
```

### Page Format (Static Content)

```json
{
  "slug": "about",
  "title": "About Us",
  "content_type": "page",
  "author": "admin",
  "status": "published",
  "blocks": [
    {
      "type": "heading",
      "data": {"level": 1, "content": "About Us"}
    },
    {
      "type": "paragraph",
      "data": {"content": "We are building..."}
    }
  ]
}
```

## Unix Gateway Pattern

```python
# Flask integration
from flask import Flask, render_template
from dbbasic_content import ContentDB

app = Flask(__name__)
content = ContentDB('/var/app/content')

@app.route('/')
def index():
    posts = content.get_posts(content_type='post', status='published', limit=10)
    return render_template('index.html', posts=posts)

@app.route('/blog/<slug>/')
def blog_post(slug):
    post = content.get_post(slug, content_type='post')
    return render_template('post.html', post=post)

@app.route('/<slug>/')
def page(slug):
    page = content.get_page(slug)
    if page:
        return render_template('page.html', page=page)
    # Fallback to article for backward compatibility
    article = content.get_post(slug, content_type='article')
    return render_template('page.html', page=article)
```

That's it. No database daemon. No migrations. Just files.

## Why This Exists

WordPress sites paying **$150K-400K/year** in hosting costs for what amounts to:
- Reading text files
- Rendering HTML
- Checking if user is logged in

This library proves you can have WordPress-level functionality with:
- ~500 lines of Python (not 500K lines of PHP)
- JSON files (not MySQL with 12+ tables)
- Unix foundations (not reinventing everything)

## The Stack

1. **dbbasic-tsv** - TSV file storage (done)
2. **dbbasic-passwd** - Unix-style user management (in progress)
3. **dbbasic-content** - Content management (this library)
4. **WordPress escape tools** - Migration toolkit (next)

## Development

```bash
# Clone and install
git clone https://github.com/quellhorst/dbbasic-content
cd dbbasic-content
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=dbbasic_content --cov-report=html
```

## License

MIT License

## Related Projects

- [dbbasic-tsv](https://github.com/askrobots/dbbasic-tsv) - TSV file database
- [dbbasic-passwd](https://github.com/askrobots/dbbasic-passwd) - Unix-style user management

## Philosophy

Read more: [Web Development's Greatest Tragedy: Rejecting Unix's Solid Foundation](https://quellhorst.com/unix-foundation-web-dev/)

---

**Start at 90% complete, not 0%**
