# Changelog

All notable changes to dbbasic-content will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-09-30

### Fixed
- Removed `dbbasic-tsv` from required dependencies (moved to optional `[tsv]` extra)
- Core package now has zero external dependencies (stdlib only)
- Fixes GitHub Actions test failures on Python 3.8/3.9

### Changed
- `dbbasic-tsv` is now optional: `pip install dbbasic-content[tsv]`
- Updated installation docs to reflect dependency changes

## [0.1.0] - 2025-09-30

### Added
- Initial release of dbbasic-content
- **ContentDB**: WordPress-like API for content management
  - `get_post()` - Get single post by slug
  - `get_posts()` - Query posts with filtering (status, categories, tags, author)
  - `create_post()` - Create new posts with blocks
  - `update_post()` - Update existing posts
  - `delete_post()` - Delete posts
  - `search()` - Full-text search across content
  - `get_categories()`, `get_tags()`, `get_authors()` - Metadata queries
- **Block System**: 8 standard block types
  - `paragraph`, `heading`, `list`, `card`, `card_list`
  - `code`, `image`, `quote`
  - Schema-based validation
  - Extensible for custom block types
- **WordPress Importer**: Migrate from WordPress to JSON blocks
  - HTML to blocks conversion
  - Full database import (posts, pages, drafts)
  - Categories and tags preservation
  - Post metadata migration
- **CLI Tools**: Unix-style commands
  - `dbcontent init` - Initialize content directory
  - `dbcontent list` - List all posts
  - `dbcontent show` - Show post details
  - `dbcontent validate` - Validate content structure
  - `dbcontent import wordpress` - Import from WordPress database
  - `dbcontent categories` - List categories
  - `dbcontent tags` - List tags
  - `dbcontent search` - Search posts
- **Documentation**:
  - Complete README with examples
  - Quick start guide
  - Flask integration examples
  - WordPress migration guide
- **Tests**: 63 tests covering all core functionality

### Philosophy
- Built on Unix foundations
- No database daemon required
- JSON files instead of MySQL
- Version control friendly
- FTP-deployable
- Grep-able content
- Start at 90% complete, not 0%

[0.1.0]: https://github.com/askrobots/dbbasic-content/releases/tag/v0.1.0
