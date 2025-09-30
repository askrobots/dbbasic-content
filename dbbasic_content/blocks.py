"""
Block definitions and validation.

Defines the block types supported by the content system.
"""

from typing import Dict, Any, List
from enum import Enum


class BlockType(str, Enum):
    """Supported block types (extensible)."""
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    LIST = "list"
    CARD = "card"
    CARD_LIST = "card_list"
    CODE = "code"
    IMAGE = "image"
    QUOTE = "quote"


# Block schemas for validation
BLOCK_SCHEMAS = {
    BlockType.PARAGRAPH: {
        "required": ["content"],
        "properties": {
            "content": {"type": "string"},
        }
    },
    BlockType.HEADING: {
        "required": ["content"],
        "properties": {
            "level": {"type": "integer", "min": 1, "max": 6},
            "content": {"type": "string"},
        }
    },
    BlockType.LIST: {
        "required": ["items"],
        "properties": {
            "listType": {"type": "string", "enum": ["ordered", "unordered"]},
            "items": {"type": "array"},
        }
    },
    BlockType.CARD: {
        "required": ["content"],
        "properties": {
            "header": {"type": "string"},
            "content": {"type": "string"},
        }
    },
    BlockType.CARD_LIST: {
        "required": ["cards"],
        "properties": {
            "cards": {"type": "array"},
        }
    },
    BlockType.CODE: {
        "required": ["code"],
        "properties": {
            "language": {"type": "string"},
            "code": {"type": "string"},
            "title": {"type": "string"},
        }
    },
    BlockType.IMAGE: {
        "required": ["src"],
        "properties": {
            "src": {"type": "string"},
            "alt": {"type": "string"},
            "caption": {"type": "string"},
        }
    },
    BlockType.QUOTE: {
        "required": ["content"],
        "properties": {
            "content": {"type": "string"},
            "author": {"type": "string"},
            "source": {"type": "string"},
        }
    },
}


def validate_block(block: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate a block structure.

    Args:
        block: Block dict with 'type' and 'data' keys

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(block, dict):
        return False, "Block must be a dictionary"

    if 'type' not in block:
        return False, "Block missing 'type' field"

    if 'data' not in block:
        return False, "Block missing 'data' field"

    block_type = block['type']
    block_data = block['data']

    # Check if block type is recognized
    if block_type not in [bt.value for bt in BlockType]:
        # Allow unknown block types (extensibility)
        return True, ""

    # Validate against schema
    schema = BLOCK_SCHEMAS.get(block_type)
    if not schema:
        return True, ""  # No schema, assume valid

    # Check required fields
    for required_field in schema.get('required', []):
        if required_field not in block_data:
            return False, f"Block type '{block_type}' requires field '{required_field}'"

    return True, ""


def validate_blocks(blocks: List[Dict[str, Any]]) -> tuple[bool, List[str]]:
    """
    Validate a list of blocks.

    Args:
        blocks: List of block dicts

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    if not isinstance(blocks, list):
        return False, ["Blocks must be a list"]

    errors = []
    for i, block in enumerate(blocks):
        is_valid, error = validate_block(block)
        if not is_valid:
            errors.append(f"Block {i}: {error}")

    return len(errors) == 0, errors
