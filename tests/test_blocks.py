"""
Tests for block validation.
"""

import pytest
from dbbasic_content.blocks import (
    BlockType,
    validate_block,
    validate_blocks,
    BLOCK_SCHEMAS
)


class TestBlockValidation:
    """Test block validation functionality."""

    def test_validate_paragraph_block(self):
        """Test validating paragraph block."""
        block = {
            'type': 'paragraph',
            'data': {'content': 'Hello world'}
        }
        is_valid, error = validate_block(block)
        assert is_valid
        assert error == ""

    def test_validate_heading_block(self):
        """Test validating heading block."""
        block = {
            'type': 'heading',
            'data': {'level': 2, 'content': 'Heading'}
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_list_block(self):
        """Test validating list block."""
        block = {
            'type': 'list',
            'data': {
                'listType': 'unordered',
                'items': ['Item 1', 'Item 2']
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_code_block(self):
        """Test validating code block."""
        block = {
            'type': 'code',
            'data': {
                'language': 'python',
                'code': 'print("hello")',
                'title': 'Example'
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_image_block(self):
        """Test validating image block."""
        block = {
            'type': 'image',
            'data': {
                'src': '/images/photo.jpg',
                'alt': 'Photo',
                'caption': 'A nice photo'
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_quote_block(self):
        """Test validating quote block."""
        block = {
            'type': 'quote',
            'data': {
                'content': 'To be or not to be',
                'author': 'Shakespeare'
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_card_block(self):
        """Test validating card block."""
        block = {
            'type': 'card',
            'data': {
                'header': 'Card Header',
                'content': 'Card content'
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_validate_card_list_block(self):
        """Test validating card_list block."""
        block = {
            'type': 'card_list',
            'data': {
                'cards': [
                    {'header': 'Card 1', 'content': 'Content 1'},
                    {'header': 'Card 2', 'content': 'Content 2'}
                ]
            }
        }
        is_valid, error = validate_block(block)
        assert is_valid

    def test_invalid_block_missing_type(self):
        """Test block without type field."""
        block = {
            'data': {'content': 'Hello'}
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "missing 'type'" in error.lower()

    def test_invalid_block_missing_data(self):
        """Test block without data field."""
        block = {
            'type': 'paragraph'
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "missing 'data'" in error.lower()

    def test_invalid_block_not_dict(self):
        """Test block that's not a dictionary."""
        block = "not a dict"
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "dictionary" in error.lower()

    def test_invalid_paragraph_missing_content(self):
        """Test paragraph block missing required content field."""
        block = {
            'type': 'paragraph',
            'data': {}
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "requires field 'content'" in error

    def test_invalid_heading_missing_content(self):
        """Test heading block missing required content field."""
        block = {
            'type': 'heading',
            'data': {'level': 2}
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "requires field 'content'" in error

    def test_invalid_list_missing_items(self):
        """Test list block missing required items field."""
        block = {
            'type': 'list',
            'data': {'listType': 'ordered'}
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "requires field 'items'" in error

    def test_invalid_code_missing_code(self):
        """Test code block missing required code field."""
        block = {
            'type': 'code',
            'data': {'language': 'python'}
        }
        is_valid, error = validate_block(block)
        assert not is_valid
        assert "requires field 'code'" in error

    def test_unknown_block_type_allowed(self):
        """Test that unknown block types are allowed (extensibility)."""
        block = {
            'type': 'custom_block_type',
            'data': {'custom': 'data'}
        }
        is_valid, error = validate_block(block)
        assert is_valid  # Unknown types are allowed

    def test_validate_blocks_list(self):
        """Test validating a list of blocks."""
        blocks = [
            {
                'type': 'paragraph',
                'data': {'content': 'Para 1'}
            },
            {
                'type': 'heading',
                'data': {'level': 2, 'content': 'Heading'}
            }
        ]
        is_valid, errors = validate_blocks(blocks)
        assert is_valid
        assert len(errors) == 0

    def test_validate_blocks_with_errors(self):
        """Test validating blocks with some invalid blocks."""
        blocks = [
            {
                'type': 'paragraph',
                'data': {'content': 'Valid'}
            },
            {
                'type': 'paragraph',
                'data': {}  # Missing content
            },
            {
                'data': {'content': 'No type'}  # Missing type
            }
        ]
        is_valid, errors = validate_blocks(blocks)
        assert not is_valid
        assert len(errors) == 2
        assert "Block 1" in errors[0]
        assert "Block 2" in errors[1]

    def test_validate_blocks_not_list(self):
        """Test validating non-list blocks."""
        blocks = "not a list"
        is_valid, errors = validate_blocks(blocks)
        assert not is_valid
        assert "must be a list" in errors[0].lower()

    def test_block_types_enum(self):
        """Test BlockType enum values."""
        assert BlockType.PARAGRAPH == "paragraph"
        assert BlockType.HEADING == "heading"
        assert BlockType.LIST == "list"
        assert BlockType.CARD == "card"
        assert BlockType.CODE == "code"
        assert BlockType.IMAGE == "image"
        assert BlockType.QUOTE == "quote"

    def test_all_block_types_have_schemas(self):
        """Test that all block types have schemas defined."""
        for block_type in BlockType:
            assert block_type in BLOCK_SCHEMAS
            schema = BLOCK_SCHEMAS[block_type]
            assert 'required' in schema
            assert 'properties' in schema
