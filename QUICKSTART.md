# Quick Start Guide

## Installation

```bash
pip install dbbasic-content

# For WordPress import
pip install dbbasic-content[wordpress]
```

## 5-Minute Tutorial

### 1. Initialize Content Directory

```bash
dbcontent init /var/app/content
```

### 2. Create Your First Post

```python
from dbbasic_content import ContentDB

content = ContentDB('/var/app/content')

content.create_post(
    slug='hello-world',
    title='Hello World',
    blocks=[
        {'type': 'paragraph', 'data': {'content': 'My first post!'}}
    ]
)
```

### 3. Retrieve Posts

```python
# Get single post
post = content.get_post('hello-world')

# Get all posts
posts = content.get_posts(status='published', limit=10)

# Get posts by category
tech_posts = content.get_posts(categories=['Technology'])

# Search
results = content.search('python')
```

### 4. Flask Integration

```python
from flask import Flask, render_template
from dbbasic_content import ContentDB

app = Flask(__name__)
content = ContentDB('/var/app/content')

@app.route('/')
def index():
    posts = content.get_posts(limit=10)
    return render_template('index.html', posts=posts)

@app.route('/<slug>/')
def post(slug):
    post = content.get_post(slug)
    return render_template('post.html', post=post)
```

## Block Types

All standard content blocks supported:

- `paragraph` - Text paragraphs
- `heading` - Headers (h1-h6)
- `list` - Ordered/unordered lists
- `code` - Syntax-highlighted code
- `image` - Images with captions
- `quote` - Blockquotes
- `card` - Content cards
- `card_list` - Multiple cards

## WordPress Migration

Import your entire WordPress site:

```bash
dbcontent import wordpress \
  --host localhost \
  --database wordpress \
  --user root \
  --password secret \
  /var/app/content
```

Or in Python:

```python
from dbbasic_content import WordPressImporter

with WordPressImporter(
    host='localhost',
    database='wordpress',
    user='root',
    password='secret'
) as importer:
    stats = importer.import_to('/var/app/content')
    print(f"Imported {stats['posts']} posts")
```

## CLI Commands

```bash
# List all posts
dbcontent list /var/app/content

# Show post details
dbcontent show /var/app/content hello-world

# Validate content structure
dbcontent validate /var/app/content

# Search
dbcontent search /var/app/content "python tutorial"

# List categories
dbcontent categories /var/app/content

# List tags
dbcontent tags /var/app/content
```

## What Makes This Different?

- **No database daemon** - just JSON files
- **Version control friendly** - commit your content
- **Grep-able** - use standard Unix tools
- **FTP-able** - deploy with rsync
- **WordPress-compatible API** - familiar methods
- **Unix foundation** - built on solid principles

## Next Steps

- See `examples/` for more usage patterns
- Read the full [README.md](README.md) for details
- Check out [Unix Foundation philosophy](https://quellhorst.com/unix-foundation-web-dev/)

---

**Start at 90% complete, not 0%**
