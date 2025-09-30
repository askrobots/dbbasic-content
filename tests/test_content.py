"""
Tests for ContentDB class.
"""

import pytest
import json
import tempfile
from pathlib import Path
from dbbasic_content import ContentDB


@pytest.fixture
def content_dir():
    """Create temporary content directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def content_db(content_dir):
    """Create ContentDB instance."""
    return ContentDB(content_dir)


@pytest.fixture
def sample_blocks():
    """Sample block content."""
    return [
        {
            'type': 'paragraph',
            'data': {'content': 'Hello world!'}
        },
        {
            'type': 'heading',
            'data': {'level': 2, 'content': 'Subheading'}
        }
    ]


class TestContentDB:
    """Test ContentDB functionality."""

    def test_init_creates_directories(self, content_dir):
        """Test that ContentDB creates necessary directories."""
        db = ContentDB(content_dir)
        articles_dir = Path(content_dir) / "articles"
        assert articles_dir.exists()
        assert articles_dir.is_dir()

    def test_create_post(self, content_db, sample_blocks):
        """Test creating a post."""
        post = content_db.create_post(
            slug='test-post',
            title='Test Post',
            blocks=sample_blocks,
            author='john',
            categories=['Technology'],
            tags=['python', 'testing']
        )

        assert post['slug'] == 'test-post'
        assert post['title'] == 'Test Post'
        assert post['author'] == 'john'
        assert post['blocks'] == sample_blocks
        assert 'Technology' in post['categories']
        assert 'python' in post['tags']

    def test_get_post(self, content_db, sample_blocks):
        """Test getting a post by slug."""
        # Create post
        content_db.create_post(
            slug='hello-world',
            title='Hello World',
            blocks=sample_blocks
        )

        # Get post
        post = content_db.get_post('hello-world')
        assert post is not None
        assert post['slug'] == 'hello-world'
        assert post['title'] == 'Hello World'

    def test_get_post_not_found(self, content_db):
        """Test getting non-existent post returns None."""
        post = content_db.get_post('does-not-exist')
        assert post is None

    def test_post_exists(self, content_db, sample_blocks):
        """Test checking if post exists."""
        assert not content_db.post_exists('test-post')

        content_db.create_post(
            slug='test-post',
            title='Test',
            blocks=sample_blocks
        )

        assert content_db.post_exists('test-post')

    def test_get_posts(self, content_db, sample_blocks):
        """Test getting multiple posts."""
        # Create multiple posts
        for i in range(5):
            content_db.create_post(
                slug=f'post-{i}',
                title=f'Post {i}',
                blocks=sample_blocks,
                status='published'
            )

        posts = content_db.get_posts()
        assert len(posts) == 5

    def test_get_posts_with_limit(self, content_db, sample_blocks):
        """Test getting posts with limit."""
        # Create posts
        for i in range(10):
            content_db.create_post(
                slug=f'post-{i}',
                title=f'Post {i}',
                blocks=sample_blocks
            )

        posts = content_db.get_posts(limit=5)
        assert len(posts) == 5

    def test_get_posts_with_offset(self, content_db, sample_blocks):
        """Test getting posts with offset."""
        # Create posts
        for i in range(10):
            content_db.create_post(
                slug=f'post-{i}',
                title=f'Post {i}',
                blocks=sample_blocks
            )

        posts = content_db.get_posts(offset=5)
        assert len(posts) == 5

    def test_get_posts_filter_by_status(self, content_db, sample_blocks):
        """Test filtering posts by status."""
        content_db.create_post(
            slug='published-post',
            title='Published',
            blocks=sample_blocks,
            status='published'
        )
        content_db.create_post(
            slug='draft-post',
            title='Draft',
            blocks=sample_blocks,
            status='draft'
        )

        published = content_db.get_posts(status='published')
        assert len(published) == 1
        assert published[0]['slug'] == 'published-post'

        drafts = content_db.get_posts(status='draft')
        assert len(drafts) == 1
        assert drafts[0]['slug'] == 'draft-post'

    def test_get_posts_filter_by_categories(self, content_db, sample_blocks):
        """Test filtering posts by categories."""
        content_db.create_post(
            slug='tech-post',
            title='Tech Post',
            blocks=sample_blocks,
            categories=['Technology']
        )
        content_db.create_post(
            slug='design-post',
            title='Design Post',
            blocks=sample_blocks,
            categories=['Design']
        )

        tech_posts = content_db.get_posts(categories=['Technology'])
        assert len(tech_posts) == 1
        assert tech_posts[0]['slug'] == 'tech-post'

    def test_get_posts_filter_by_tags(self, content_db, sample_blocks):
        """Test filtering posts by tags."""
        content_db.create_post(
            slug='python-post',
            title='Python Post',
            blocks=sample_blocks,
            tags=['python']
        )
        content_db.create_post(
            slug='javascript-post',
            title='JavaScript Post',
            blocks=sample_blocks,
            tags=['javascript']
        )

        python_posts = content_db.get_posts(tags=['python'])
        assert len(python_posts) == 1
        assert python_posts[0]['slug'] == 'python-post'

    def test_get_posts_filter_by_author(self, content_db, sample_blocks):
        """Test filtering posts by author."""
        content_db.create_post(
            slug='john-post',
            title='John Post',
            blocks=sample_blocks,
            author='john'
        )
        content_db.create_post(
            slug='jane-post',
            title='Jane Post',
            blocks=sample_blocks,
            author='jane'
        )

        john_posts = content_db.get_posts(author='john')
        assert len(john_posts) == 1
        assert john_posts[0]['slug'] == 'john-post'

    def test_update_post(self, content_db, sample_blocks):
        """Test updating a post."""
        # Create post
        content_db.create_post(
            slug='test-post',
            title='Original Title',
            blocks=sample_blocks
        )

        # Update post
        updated = content_db.update_post(
            'test-post',
            title='Updated Title',
            status='draft'
        )

        assert updated['title'] == 'Updated Title'
        assert updated['status'] == 'draft'

        # Verify persistence
        post = content_db.get_post('test-post')
        assert post['title'] == 'Updated Title'

    def test_update_post_not_found(self, content_db):
        """Test updating non-existent post returns None."""
        result = content_db.update_post('does-not-exist', title='New Title')
        assert result is None

    def test_delete_post(self, content_db, sample_blocks):
        """Test deleting a post."""
        # Create post
        content_db.create_post(
            slug='test-post',
            title='Test',
            blocks=sample_blocks
        )

        assert content_db.post_exists('test-post')

        # Delete post
        result = content_db.delete_post('test-post')
        assert result is True
        assert not content_db.post_exists('test-post')

    def test_delete_post_not_found(self, content_db):
        """Test deleting non-existent post returns False."""
        result = content_db.delete_post('does-not-exist')
        assert result is False

    def test_get_categories(self, content_db, sample_blocks):
        """Test getting all categories."""
        content_db.create_post(
            slug='post-1',
            title='Post 1',
            blocks=sample_blocks,
            categories=['Technology', 'Python']
        )
        content_db.create_post(
            slug='post-2',
            title='Post 2',
            blocks=sample_blocks,
            categories=['Design', 'Python']
        )

        categories = content_db.get_categories()
        assert 'Technology' in categories
        assert 'Design' in categories
        assert 'Python' in categories
        assert len(categories) == 3

    def test_get_tags(self, content_db, sample_blocks):
        """Test getting all tags."""
        content_db.create_post(
            slug='post-1',
            title='Post 1',
            blocks=sample_blocks,
            tags=['python', 'flask']
        )
        content_db.create_post(
            slug='post-2',
            title='Post 2',
            blocks=sample_blocks,
            tags=['javascript', 'python']
        )

        tags = content_db.get_tags()
        assert 'python' in tags
        assert 'flask' in tags
        assert 'javascript' in tags
        assert len(tags) == 3

    def test_get_authors(self, content_db, sample_blocks):
        """Test getting all authors."""
        content_db.create_post(
            slug='post-1',
            title='Post 1',
            blocks=sample_blocks,
            author='john'
        )
        content_db.create_post(
            slug='post-2',
            title='Post 2',
            blocks=sample_blocks,
            author='jane'
        )

        authors = content_db.get_authors()
        assert 'john' in authors
        assert 'jane' in authors
        assert len(authors) == 2

    def test_search_by_title(self, content_db, sample_blocks):
        """Test searching posts by title."""
        content_db.create_post(
            slug='python-tutorial',
            title='Python Tutorial',
            blocks=sample_blocks
        )
        content_db.create_post(
            slug='javascript-guide',
            title='JavaScript Guide',
            blocks=sample_blocks
        )

        results = content_db.search('Python')
        assert len(results) == 1
        assert results[0]['slug'] == 'python-tutorial'

    def test_search_by_content(self, content_db):
        """Test searching posts by content."""
        content_db.create_post(
            slug='post-1',
            title='Post 1',
            blocks=[
                {'type': 'paragraph', 'data': {'content': 'This is about Python programming'}}
            ]
        )
        content_db.create_post(
            slug='post-2',
            title='Post 2',
            blocks=[
                {'type': 'paragraph', 'data': {'content': 'This is about JavaScript'}}
            ]
        )

        results = content_db.search('Python')
        assert len(results) == 1
        assert results[0]['slug'] == 'post-1'

    def test_search_case_insensitive(self, content_db, sample_blocks):
        """Test search is case insensitive."""
        content_db.create_post(
            slug='test-post',
            title='Test Post',
            blocks=sample_blocks
        )

        results = content_db.search('test')
        assert len(results) == 1

        results = content_db.search('TEST')
        assert len(results) == 1

        results = content_db.search('TeSt')
        assert len(results) == 1

    def test_post_ordering(self, content_db, sample_blocks):
        """Test posts are ordered by date descending by default."""
        content_db.create_post(
            slug='post-1',
            title='Post 1',
            date='2025-01-01',
            blocks=sample_blocks
        )
        content_db.create_post(
            slug='post-2',
            title='Post 2',
            date='2025-01-15',
            blocks=sample_blocks
        )
        content_db.create_post(
            slug='post-3',
            title='Post 3',
            date='2025-01-10',
            blocks=sample_blocks
        )

        posts = content_db.get_posts(order_by='date', order='desc')
        assert posts[0]['slug'] == 'post-2'  # Most recent
        assert posts[1]['slug'] == 'post-3'
        assert posts[2]['slug'] == 'post-1'  # Oldest
