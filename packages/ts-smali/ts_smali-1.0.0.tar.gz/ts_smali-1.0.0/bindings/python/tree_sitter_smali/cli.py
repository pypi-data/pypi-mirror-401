"""Command-line interface for tree-sitter-smali."""

import sys
from pathlib import Path


def print_highlights():
    """Print the highlights.scm query file."""
    highlights_content = None
    
    # Try to find queries using importlib.resources (for installed packages)
    try:
        # Python 3.9+ has importlib.resources.files
        try:
            from importlib.resources import files
            highlights_content = (files("tree_sitter_smali") / "queries" / "highlights.scm").read_text(encoding="utf-8")
        except (ImportError, FileNotFoundError, AttributeError):
            # Fallback for Python < 3.9 or if files() doesn't work
            try:
                import importlib.resources as pkg_resources
                highlights_content = pkg_resources.read_text("tree_sitter_smali.queries", "highlights.scm", encoding="utf-8")
            except (ImportError, FileNotFoundError):
                pass
    except Exception:
        pass
    
    # If not found via importlib, try filesystem paths
    if highlights_content is None:
        package_dir = Path(__file__).parent
        
        # Try package directory (installed package or editable install with queries copied)
        queries_dir = package_dir / "queries"
        highlights_file = queries_dir / "highlights.scm"
        
        if highlights_file.exists():
            with open(highlights_file, "r", encoding="utf-8") as f:
                highlights_content = f.read()
        
        # If still not found, try project root (development mode)
        if highlights_content is None:
            # Go up from bindings/python/tree_sitter_smali to project root
            project_root = package_dir.parent.parent.parent
            queries_dir = project_root / "queries"
            highlights_file = queries_dir / "highlights.scm"
            
            if highlights_file.exists():
                with open(highlights_file, "r", encoding="utf-8") as f:
                    highlights_content = f.read()
    
    if highlights_content is None:
        print("Error: highlights.scm not found", file=sys.stderr)
        print("  Tried: importlib.resources", file=sys.stderr)
        print(f"  Tried: {Path(__file__).parent / 'queries' / 'highlights.scm'}", file=sys.stderr)
        package_dir = Path(__file__).parent
        project_root = package_dir.parent.parent.parent
        print(f"  Tried: {project_root / 'queries' / 'highlights.scm'}", file=sys.stderr)
        sys.exit(1)
    
    print(highlights_content, end="")


if __name__ == "__main__":
    print_highlights()
