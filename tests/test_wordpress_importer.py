"""
Tests for WordPress importer.
"""

import pytest
from dbbasic_content.wordpress_importer import (
    HTMLToBlocksParser,
    WordPressImporter
)


class TestHTMLToBlocksParser:
    """Test HTML to blocks conversion."""

    def test_parse_paragraph(self):
        """Test parsing paragraph tags."""
        parser = HTMLToBlocksParser()
        parser.feed('<p>Hello world</p>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'paragraph'
        assert blocks[0]['data']['content'] == 'Hello world'

    def test_parse_multiple_paragraphs(self):
        """Test parsing multiple paragraphs."""
        parser = HTMLToBlocksParser()
        parser.feed('<p>First paragraph</p><p>Second paragraph</p>')
        blocks = parser.get_blocks()

        assert len(blocks) == 2
        assert blocks[0]['data']['content'] == 'First paragraph'
        assert blocks[1]['data']['content'] == 'Second paragraph'

    def test_parse_heading(self):
        """Test parsing heading tags."""
        parser = HTMLToBlocksParser()
        parser.feed('<h2>My Heading</h2>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'heading'
        assert blocks[0]['data']['level'] == 2
        assert blocks[0]['data']['content'] == 'My Heading'

    def test_parse_multiple_heading_levels(self):
        """Test parsing different heading levels."""
        for level in range(1, 7):
            parser = HTMLToBlocksParser()
            parser.feed(f'<h{level}>Heading</h{level}>')
            blocks = parser.get_blocks()

            assert blocks[0]['type'] == 'heading'
            assert blocks[0]['data']['level'] == level

    def test_parse_unordered_list(self):
        """Test parsing unordered list."""
        parser = HTMLToBlocksParser()
        parser.feed('<ul><li>Item 1</li><li>Item 2</li></ul>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'list'
        assert blocks[0]['data']['listType'] == 'unordered'
        assert blocks[0]['data']['items'] == ['Item 1', 'Item 2']

    def test_parse_ordered_list(self):
        """Test parsing ordered list."""
        parser = HTMLToBlocksParser()
        parser.feed('<ol><li>First</li><li>Second</li></ol>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'list'
        assert blocks[0]['data']['listType'] == 'ordered'
        assert blocks[0]['data']['items'] == ['First', 'Second']

    def test_parse_blockquote(self):
        """Test parsing blockquote."""
        parser = HTMLToBlocksParser()
        parser.feed('<blockquote>A quote</blockquote>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'quote'
        assert blocks[0]['data']['content'] == 'A quote'

    def test_parse_code_block(self):
        """Test parsing pre/code tags."""
        parser = HTMLToBlocksParser()
        parser.feed('<pre>print("hello")</pre>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'code'
        assert blocks[0]['data']['code'] == 'print("hello")'
        assert blocks[0]['data']['language'] == 'text'

    def test_parse_mixed_content(self):
        """Test parsing mixed content types."""
        html = '''
        <h1>Title</h1>
        <p>First paragraph</p>
        <p>Second paragraph</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        '''
        parser = HTMLToBlocksParser()
        parser.feed(html)
        blocks = parser.get_blocks()

        assert len(blocks) == 4
        assert blocks[0]['type'] == 'heading'
        assert blocks[1]['type'] == 'paragraph'
        assert blocks[2]['type'] == 'paragraph'
        assert blocks[3]['type'] == 'list'

    def test_parse_empty_content(self):
        """Test parsing empty content."""
        parser = HTMLToBlocksParser()
        parser.feed('')
        blocks = parser.get_blocks()

        assert len(blocks) == 0

    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only content."""
        parser = HTMLToBlocksParser()
        parser.feed('   \n\n   ')
        blocks = parser.get_blocks()

        assert len(blocks) == 0

    def test_parse_plain_text(self):
        """Test parsing plain text without tags."""
        parser = HTMLToBlocksParser()
        parser.feed('Just plain text')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'paragraph'
        assert blocks[0]['data']['content'] == 'Just plain text'

    def test_ignore_empty_paragraphs(self):
        """Test that empty paragraphs are ignored."""
        parser = HTMLToBlocksParser()
        parser.feed('<p></p><p>Content</p><p>  </p>')
        blocks = parser.get_blocks()

        assert len(blocks) == 1
        assert blocks[0]['data']['content'] == 'Content'

    def test_strip_whitespace(self):
        """Test that whitespace is properly stripped."""
        parser = HTMLToBlocksParser()
        parser.feed('<p>  Content with spaces  </p>')
        blocks = parser.get_blocks()

        assert blocks[0]['data']['content'] == 'Content with spaces'


class TestWordPressImporterUnit:
    """Unit tests for WordPressImporter (no database required)."""

    def test_convert_empty_content(self):
        """Test converting empty content."""
        importer = WordPressImporter()
        blocks = importer._convert_content_to_blocks('')
        assert blocks == []

    def test_convert_simple_content(self):
        """Test converting simple HTML content."""
        importer = WordPressImporter()
        html = '<p>Hello world</p>'
        blocks = importer._convert_content_to_blocks(html)

        assert len(blocks) == 1
        assert blocks[0]['type'] == 'paragraph'

    def test_convert_complex_content(self):
        """Test converting complex HTML content."""
        importer = WordPressImporter()
        html = '''
        <h1>Title</h1>
        <p>Introduction paragraph</p>
        <ul>
            <li>Point 1</li>
            <li>Point 2</li>
        </ul>
        '''
        blocks = importer._convert_content_to_blocks(html)

        assert len(blocks) >= 3
        assert any(b['type'] == 'heading' for b in blocks)
        assert any(b['type'] == 'paragraph' for b in blocks)
        assert any(b['type'] == 'list' for b in blocks)

    def test_importer_context_manager(self):
        """Test using importer as context manager."""
        with WordPressImporter() as importer:
            assert importer is not None
            assert importer._connection is None  # Not connected yet

    def test_importer_initialization(self):
        """Test importer initialization with custom params."""
        importer = WordPressImporter(
            host='localhost',
            database='wp_db',
            user='wp_user',
            password='wp_pass',
            port=3307,
            table_prefix='custom_'
        )

        assert importer.host == 'localhost'
        assert importer.database == 'wp_db'
        assert importer.user == 'wp_user'
        assert importer.password == 'wp_pass'
        assert importer.port == 3307
        assert importer.table_prefix == 'custom_'


# Integration tests would require actual WordPress database
# These would be in a separate test file: test_wordpress_importer_integration.py
