"""
Pytest tests for tree-sitter-smali with JSON snapshot comparison.

This test suite parses Smali files and compares the resulting syntax trees
against stored JSON snapshots to ensure parsing consistency.
"""

import json
import warnings
from pathlib import Path
from typing import Dict, Any

import pytest
from tree_sitter import Parser, Language
from tree_sitter_smali import language


def node_to_dict(node) -> Dict[str, Any]:
    """
    Convert a tree-sitter node to a dictionary representation.
    
    This creates a serializable JSON structure containing:
    - Node type
    - Byte positions (start_byte, end_byte)
    - Point positions (start_point, end_point)
    - All child nodes (recursively)
    
    Args:
        node: A tree-sitter Node object
        
    Returns:
        Dictionary representation of the node and its children
    """
    return {
        'type': node.type,
        'start_byte': node.start_byte,
        'end_byte': node.end_byte,
        'start_point': {'row': node.start_point[0], 'column': node.start_point[1]},
        'end_point': {'row': node.end_point[0], 'column': node.end_point[1]},
        'children': [node_to_dict(child) for child in node.children]
    }


def parse_smali_file(file_path: Path) -> Any:
    """
    Parse a Smali file and return the syntax tree.
    
    Args:
        file_path: Path to the Smali file to parse
        
    Returns:
        Tree-sitter Tree object
    """
    # Suppress deprecation warning for Language(int) usage
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        lang = Language(language())
    parser = Parser(lang)
    
    with open(file_path, 'rb') as f:
        code = f.read()
    
    tree = parser.parse(code)
    return tree


def load_snapshot(snapshot_path: Path) -> Dict[str, Any]:
    """
    Load a JSON snapshot from disk.
    
    Args:
        snapshot_path: Path to the JSON snapshot file
        
    Returns:
        Dictionary containing the snapshot data
    """
    if not snapshot_path.exists():
        return None
    
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_snapshot(snapshot_path: Path, tree_dict: Dict[str, Any]) -> None:
    """
    Save a tree dictionary to a JSON snapshot file.
    
    Args:
        snapshot_path: Path where to save the snapshot
        tree_dict: Dictionary representation of the tree
    """
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    with open(snapshot_path, 'w', encoding='utf-8') as f:
        json.dump(tree_dict, f, indent=2, ensure_ascii=False)


def compare_trees(current: Dict[str, Any], expected: Dict[str, Any], path: str = "root") -> list:
    """
    Compare two tree dictionaries and return a list of differences.
    
    Args:
        current: Current tree dictionary
        expected: Expected tree dictionary
        path: Current path in the tree (for error reporting)
        
    Returns:
        List of difference descriptions
    """
    differences = []
    
    if current['type'] != expected['type']:
        differences.append(f"{path}: type mismatch - got '{current['type']}', expected '{expected['type']}'")
    
    if current['start_byte'] != expected['start_byte']:
        differences.append(f"{path}: start_byte mismatch - got {current['start_byte']}, expected {expected['start_byte']}")
    
    if current['end_byte'] != expected['end_byte']:
        differences.append(f"{path}: end_byte mismatch - got {current['end_byte']}, expected {expected['end_byte']}")
    
    if current['start_point'] != expected['start_point']:
        differences.append(f"{path}: start_point mismatch - got {current['start_point']}, expected {expected['start_point']}")
    
    if current['end_point'] != expected['end_point']:
        differences.append(f"{path}: end_point mismatch - got {current['end_point']}, expected {expected['end_point']}")
    
    current_children = current.get('children', [])
    expected_children = expected.get('children', [])
    
    if len(current_children) != len(expected_children):
        differences.append(
            f"{path}: children count mismatch - got {len(current_children)}, expected {len(expected_children)}"
        )
    
    min_children = min(len(current_children), len(expected_children))
    for i in range(min_children):
        child_diffs = compare_trees(current_children[i], expected_children[i], f"{path}.children[{i}]")
        differences.extend(child_diffs)
    
    if len(current_children) > len(expected_children):
        for i in range(min_children, len(current_children)):
            differences.append(f"{path}.children[{i}]: unexpected child node of type '{current_children[i]['type']}'")
    
    if len(expected_children) > len(current_children):
        for i in range(min_children, len(expected_children)):
            differences.append(f"{path}.children[{i}]: missing expected child node of type '{expected_children[i]['type']}'")
    
    return differences


# Test fixtures
@pytest.fixture
def test_dir() -> Path:
    """Get the test directory path."""
    return Path(__file__).parent


@pytest.fixture
def snapshots_dir(test_dir: Path) -> Path:
    """Get the snapshots directory path."""
    return test_dir / "snapshots"


@pytest.fixture
def test_files(test_dir: Path) -> list:
    """Get list of test Smali files."""
    return [
        test_dir / "test_sample.smali",
        test_dir / "test_comprehensive.smali",
    ]


# Test cases
def test_parse_basic_file(test_dir: Path):
    """Test that we can parse the basic test Smali file."""
    test_file = test_dir / "test_sample.smali"
    assert test_file.exists(), f"Test file not found: {test_file}"
    
    tree = parse_smali_file(test_file)
    assert tree is not None
    assert tree.root_node is not None
    assert tree.root_node.type is not None


def test_parse_comprehensive_file(test_dir: Path):
    """Test that we can parse the comprehensive test Smali file."""
    test_file = test_dir / "test_comprehensive.smali"
    assert test_file.exists(), f"Test file not found: {test_file}"
    
    tree = parse_smali_file(test_file)
    assert tree is not None
    assert tree.root_node is not None
    assert tree.root_node.type is not None


def test_tree_structure_validation(test_dir: Path):
    """Test basic tree structure properties."""
    test_file = test_dir / "test_sample.smali"
    tree = parse_smali_file(test_file)
    root = tree.root_node
    
    # Verify root node
    assert root.type is not None
    assert root.start_byte == 0
    assert root.end_byte > 0
    
    # Verify it has children
    assert len(root.children) > 0
    
    # Check that all nodes have valid byte ranges
    def check_node(node):
        assert node.start_byte <= node.end_byte
        assert node.start_point[0] <= node.end_point[0] or (
            node.start_point[0] == node.end_point[0] and 
            node.start_point[1] <= node.end_point[1]
        )
        for child in node.children:
            check_node(child)
    
    check_node(root)


@pytest.mark.parametrize("test_file_name", [
    "test_sample.smali",
    "test_comprehensive.smali",
])
def test_syntax_tree_snapshot(test_dir: Path, snapshots_dir: Path, test_file_name: str):
    """
    Test that the syntax tree matches the saved snapshot.
    
    This test parses a Smali file and compares the resulting tree structure
    against a stored JSON snapshot. If the snapshot doesn't exist, it will
    be created automatically.
    """
    test_file = test_dir / test_file_name
    snapshot_file = snapshots_dir / f"{test_file_name}.json"
    
    assert test_file.exists(), f"Test file not found: {test_file}"
    
    # Parse the Smali file
    tree = parse_smali_file(test_file)
    current_tree_dict = node_to_dict(tree.root_node)
    
    # Load snapshot if it exists
    expected_tree_dict = load_snapshot(snapshot_file)
    
    if expected_tree_dict is None:
        # Create initial snapshot
        save_snapshot(snapshot_file, current_tree_dict)
        pytest.fail(
            f"Snapshot file created: {snapshot_file}\n"
            f"Run the test again to verify the snapshot is correct."
        )
    else:
        # Compare trees
        differences = compare_trees(current_tree_dict, expected_tree_dict)
        
        if differences:
            # Save the current tree for debugging
            debug_file = snapshot_file.with_suffix('.current.json')
            save_snapshot(debug_file, current_tree_dict)
            
            error_msg = (
                f"Syntax tree has changed for {test_file_name}!\n"
                f"Found {len(differences)} difference(s):\n"
            )
            error_msg += "\n".join(f"  - {diff}" for diff in differences[:20])  # Limit to first 20
            if len(differences) > 20:
                error_msg += f"\n  ... and {len(differences) - 20} more differences"
            error_msg += (
                f"\n\nCurrent tree saved to: {debug_file}\n"
                f"To update the snapshot, delete {snapshot_file} and run the test again, "
                f"or manually copy {debug_file} to {snapshot_file}"
            )
            pytest.fail(error_msg)


def test_all_nodes_have_valid_ranges(test_dir: Path):
    """Test that all nodes in the tree have valid byte and point ranges."""
    test_file = test_dir / "test_comprehensive.smali"
    tree = parse_smali_file(test_file)
    
    def validate_node(node, parent_end_byte=None):
        """Recursively validate node ranges."""
        # Check byte ranges
        assert node.start_byte >= 0, f"Node {node.type} has negative start_byte"
        assert node.end_byte >= node.start_byte, f"Node {node.type} has invalid byte range"
        
        # Check point ranges
        assert node.start_point[0] >= 0, f"Node {node.type} has negative start row"
        assert node.start_point[1] >= 0, f"Node {node.type} has negative start column"
        
        # Check that children are within parent
        if parent_end_byte is not None:
            assert node.start_byte >= 0, f"Node {node.type} starts before parent"
            assert node.end_byte <= parent_end_byte, f"Node {node.type} extends beyond parent"
        
        # Validate children
        for child in node.children:
            validate_node(child, node.end_byte)
    
    validate_node(tree.root_node)
