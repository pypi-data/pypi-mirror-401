"""Pytest tests for tree-sitter-kotlin syntax tree parsing."""

import json
import warnings
import pytest
from pathlib import Path
from tree_sitter import Parser, Language
from tree_sitter_kotlin import language


def node_to_dict(node):
    """Convert a tree-sitter node to a dictionary representation."""
    return {
        'type': node.type,
        'start_byte': node.start_byte,
        'end_byte': node.end_byte,
        'start_point': {'row': node.start_point[0], 'column': node.start_point[1]},
        'end_point': {'row': node.end_point[0], 'column': node.end_point[1]},
        'children': [node_to_dict(child) for child in node.children]
    }


def parse_kotlin_file(file_path):
    """Parse a Kotlin file and return the syntax tree."""
    # Suppress deprecation warning for Language(int) usage
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        lang = Language(language())
    parser = Parser(lang)
    
    with open(file_path, 'rb') as f:
        code = f.read()
    
    tree = parser.parse(code)
    return tree


@pytest.fixture
def test_kotlin_file():
    """Path to the test Kotlin file."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "test" / "test_sample.kt"


@pytest.fixture
def snapshot_file():
    """Path to the snapshot file."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "test" / "test_sample_tree.json"


def test_parse_kotlin_file(test_kotlin_file):
    """Test that we can parse the Kotlin test file."""
    assert test_kotlin_file.exists(), f"Test file not found: {test_kotlin_file}"
    
    tree = parse_kotlin_file(test_kotlin_file)
    assert tree is not None
    assert tree.root_node is not None
    assert tree.root_node.type == "source_file"


def test_syntax_tree_snapshot(test_kotlin_file, snapshot_file):
    """Test that the syntax tree matches the saved snapshot."""
    # Parse the Kotlin file
    tree = parse_kotlin_file(test_kotlin_file)
    current_tree_dict = node_to_dict(tree.root_node)
    
    # Load snapshot if it exists, otherwise create it
    if snapshot_file.exists():
        with open(snapshot_file, 'r') as f:
            stored_tree_dict = json.load(f)
        
        assert current_tree_dict == stored_tree_dict, \
            f"Syntax tree has changed! Update snapshot with: pytest test/test_syntax_tree.py::test_syntax_tree_snapshot --snapshot-update"
    else:
        # Create initial snapshot
        with open(snapshot_file, 'w') as f:
            json.dump(current_tree_dict, f, indent=2)
        pytest.fail(f"Snapshot file created: {snapshot_file}. Run the test again to verify.")


def test_tree_structure(test_kotlin_file):
    """Test basic tree structure properties."""
    tree = parse_kotlin_file(test_kotlin_file)
    root = tree.root_node
    
    # Verify root node
    assert root.type == "source_file"
    assert root.start_byte == 0
    assert root.end_byte > 0
    
    # Verify it has children (package, class, function, etc.)
    assert len(root.children) > 0
    
    # Check that all nodes have valid byte ranges
    def check_node(node):
        assert node.start_byte <= node.end_byte
        for child in node.children:
            check_node(child)
    
    check_node(root)
