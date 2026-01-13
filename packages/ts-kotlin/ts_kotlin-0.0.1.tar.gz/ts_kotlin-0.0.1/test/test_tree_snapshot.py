#!/usr/bin/env python3
"""
Test script that parses a Kotlin file and verifies the syntax tree hasn't changed.

Usage:
    python test_tree_snapshot.py [--update]

    --update: Update the snapshot file if the tree has changed
"""

import sys
import json
import argparse
from pathlib import Path

try:
    from tree_sitter import Parser
    from tree_sitter_kotlin import language
except ImportError as e:
    print(f"Error: {e}", file=sys.stderr)
    print("Please install tree-sitter and ts-kotlin:", file=sys.stderr)
    print("  pip install tree-sitter ts-kotlin", file=sys.stderr)
    sys.exit(1)


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


def tree_to_string(node, source_bytes=None, indent=0):
    """Convert a tree-sitter node to a string representation (S-expression style)."""
    prefix = "  " * indent
    result = f"{prefix}({node.type}"
    
    if not node.children and source_bytes:
        # Leaf node - include text if it's short
        text = source_bytes[node.start_byte:node.end_byte].decode('utf-8', errors='replace')
        if text and len(text) < 50 and '\n' not in text:
            result += f" {text!r}"
    
    for child in node.children:
        result += "\n" + tree_to_string(child, source_bytes, indent + 1)
    
    result += ")"
    return result


def parse_kotlin_file(file_path):
    """Parse a Kotlin file and return the syntax tree."""
    parser = Parser()
    parser.set_language(language)
    
    with open(file_path, 'rb') as f:
        code = f.read()
    
    tree = parser.parse(code)
    return tree


def main():
    parser = argparse.ArgumentParser(
        description='Test that the Kotlin syntax tree has not changed'
    )
    parser.add_argument(
        '--update',
        action='store_true',
        help='Update the snapshot file if the tree has changed'
    )
    parser.add_argument(
        '--kotlin-file',
        type=str,
        default=None,
        help='Path to the Kotlin test file (default: test/test_sample.kt)'
    )
    parser.add_argument(
        '--snapshot-file',
        type=str,
        default=None,
        help='Path to the snapshot file (default: test/test_sample_tree.json)'
    )
    
    args = parser.parse_args()
    
    # Get absolute paths - script is in test/, so parent is project root
    script_dir = Path(__file__).parent.parent
    kotlin_file = script_dir / (args.kotlin_file or 'test/test_sample.kt')
    snapshot_file = script_dir / (args.snapshot_file or 'test/test_sample_tree.json')
    
    if not kotlin_file.exists():
        print(f"Error: Kotlin file not found: {kotlin_file}", file=sys.stderr)
        sys.exit(1)
    
    # Parse the Kotlin file
    print(f"Parsing {kotlin_file}...")
    tree = parse_kotlin_file(kotlin_file)
    
    # Read source for text display
    with open(kotlin_file, 'rb') as f:
        source_bytes = f.read()
    
    # Convert to dictionary for comparison
    current_tree_dict = node_to_dict(tree.root_node)
    
    # Print the tree structure
    print("\nCurrent syntax tree:")
    print("=" * 80)
    print(tree_to_string(tree.root_node, source_bytes))
    print("=" * 80)
    
    # Check against snapshot
    if snapshot_file.exists():
        with open(snapshot_file, 'r') as f:
            stored_tree_dict = json.load(f)
        
        if current_tree_dict == stored_tree_dict:
            print("\n✓ The syntax tree has not changed. Test passed!")
            return 0
        else:
            print("\n✗ The syntax tree has changed!")
            
            if args.update:
                # Update the snapshot
                with open(snapshot_file, 'w') as f:
                    json.dump(current_tree_dict, f, indent=2)
                print(f"✓ Snapshot updated: {snapshot_file}")
                return 0
            else:
                print(f"\nTo update the snapshot, run:")
                print(f"  python {Path(__file__).name} --update")
                return 1
    else:
        # No snapshot exists, create one
        print(f"\nNo snapshot found. Creating initial snapshot: {snapshot_file}")
        with open(snapshot_file, 'w') as f:
            json.dump(current_tree_dict, f, indent=2)
        print("✓ Snapshot created successfully!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
