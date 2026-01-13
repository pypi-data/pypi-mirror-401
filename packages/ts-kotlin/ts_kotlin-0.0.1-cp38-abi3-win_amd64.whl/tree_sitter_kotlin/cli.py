"""Command-line interface for tree-sitter-kotlin."""

import sys
from pathlib import Path


def print_highlights():
    """Print the highlights.scm query file."""
    # Get the package directory
    package_dir = Path(__file__).parent
    queries_dir = package_dir / "queries"
    highlights_file = queries_dir / "highlights.scm"
    
    if not highlights_file.exists():
        print(f"Error: highlights.scm not found at {highlights_file}", file=sys.stderr)
        sys.exit(1)
    
    # Read and print the file
    with open(highlights_file, "r", encoding="utf-8") as f:
        print(f.read(), end="")


if __name__ == "__main__":
    print_highlights()
