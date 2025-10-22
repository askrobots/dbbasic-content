# Pages Support - Changelog

## Overview

Added support for WordPress-style **pages** in addition to **posts**, allowing dbbasic-content to handle both blog content (posts) and static content (pages) separately.

## What Changed

### 1. New Directory Structure

```
/var/app/content/
├── articles/          # Legacy (backward compatible)
├── posts/             # NEW: Blog posts (dated, categorized)
├── pages/             # NEW: Static pages (no date/categories)
├── metadata.tsv
└── taxonomy.tsv
```

### 2. Content Type System

All content now has a `content_type` field:
- `"post"` - Blog articles (dated, categorized)
- `"page"` - Static pages (no dates, no categories)
- `"article"` - Legacy (for backward compatibility)

### 3. New API Methods

**Page-specific methods:**
```python
# Create
content.create_page(slug, title, blocks, ...)

# Read
content.get_page(slug)
content.get_pages(status=None, limit=None, ...)

# Update
content.update_page(slug, **updates)

# Delete
content.delete_page(slug)

# Check existence
content.page_exists(slug)
```

**Enhanced existing methods:**
```python
# All existing methods now accept content_type parameter
content.get_post(slug, content_type='article')  # Default for backward compat
content.get_posts(content_type='post', ...)
content.create_post(slug, title, blocks, content_type='post', ...)
content.update_post(slug, content_type='article', ...)
content.delete_post(slug, content_type='article')
content.post_exists(slug, content_type='article')
```

### 4. Posts vs Pages

**Posts (Blog Articles)**
- Have publication dates
- Support categories and tags
- Displayed chronologically (newest first)
- Used for: Blog posts, news articles, announcements

**Pages (Static Content)**
- No dates (timeless content)
- No categories or tags
- Displayed alphabetically or by menu order
- Used for: About, Contact, Documentation, Specs

### 5. File Changes

**Modified:**
- `dbbasic_content/content.py` - Added page support and content_type system
- `tests/test_content.py` - Added comprehensive page tests (9 new tests)
- `README.md` - Updated with page examples and documentation
- `examples/` - Added `pages_example.py` demonstration

**Backward Compatibility:**
- All existing code continues to work
- Default `content_type='article'` for all methods
- Existing `articles/` directory still used by default

## Use Cases

### For dbbasic-public Project

Perfect for sites with both dynamic and static content:

```python
content = ContentDB('/var/app/content')

# Blog posts
content.create_post(
    slug='announcing-dbbasic',
    title='Announcing DBBasic',
    content_type='post',
    date='2025-10-22',
    categories=['Announcements'],
    blocks=[...]
)

# Documentation pages
content.create_page(
    slug='sessions-spec',
    title='dbbasic-sessions Specification',
    blocks=[...]
)

content.create_page(
    slug='queue-spec',
    title='dbbasic-queue Specification',
    blocks=[...]
)

# List all specs (pages)
specs = content.get_pages()

# List all blog posts
posts = content.get_posts(content_type='post')
```

## Testing

All 72 tests pass:
- 23 existing content tests (backward compatible)
- 9 new page-specific tests
- 40 other tests (blocks, WordPress importer)

Run tests:
```bash
pytest tests/ -v
```

## Migration Path

### Option 1: Keep using articles/ (no changes needed)
```python
# Continue using default behavior
content.get_posts()  # Uses articles/ directory
```

### Option 2: Migrate to posts/pages
```python
# Move blog content to posts/
for article in old_articles:
    content.create_post(
        content_type='post',
        ...
    )

# Move static content to pages/
for static_page in static_content:
    content.create_page(
        ...
    )
```

## Example Output

```
Directory Structure:
--------------------
posts/
  - getting-started.json
  - announcing-v1.json
pages/
  - api-docs.json
  - contact.json
  - about.json

Blog Posts (chronological):
---------------------------
[2025-10-21] Getting Started with DBBasic
  Categories: Tutorials
  Tags: tutorial, beginner

[2025-10-20] Announcing Version 1.0
  Categories: Announcements, Releases
  Tags: v1, release

Static Pages (alphabetical):
----------------------------
API Documentation
  Slug: api-docs
  Type: page

About DBBasic
  Slug: about
  Type: page
```

## Benefits

1. **Clear separation** - Blog posts vs static pages
2. **WordPress-like** - Familiar mental model
3. **Backward compatible** - Existing code works unchanged
4. **Unix-friendly** - Still just JSON files on disk
5. **Type-safe** - content_type field prevents confusion
6. **Same slug space** - Can have post/hello-world and page/hello-world

## Next Steps

For dbbasic-public integration:
1. Use pages for specifications (SESSIONS_SPEC, QUEUE_SPEC, etc.)
2. Use posts for blog content and announcements
3. Keep clean separation between content types
4. Enjoy simple filesystem-based CMS!
