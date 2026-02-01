"""
Contains utility functions used across the package.
"""

import os
from pathlib import Path

from .models import Match
from .types import PathMap

# MARK: Functions


def match_paths(path_map: PathMap) -> list[Match]:
    """Determines which relative paths are shared between the directories."""
    temporary: dict[str, list[str]] = {}
    for base_path, relative_paths in path_map.items():
        for relative_path in relative_paths:
            temporary.setdefault(relative_path, []).append(base_path)
    return [Match(bases, relative) for relative, bases in temporary.items()]


def combine_directory_structures(
    input_directories: list[str],
    output_directory: str,
) -> None:
    """Combine structures of input directories into an output directory."""

    # Create a set of all unique subdirectory paths
    subdirectories = set()
    for input_directory in input_directories:
        for directory_path, directory_names, _ in os.walk(input_directory):
            relative_path = Path(directory_path).relative_to(input_directory)
            for directory_name in directory_names:
                subdirectories.add(relative_path / directory_name)

    # Create the output directory and any subdirectories
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    for subdirectory in subdirectories:
        new_subdirectory_path = Path(output_directory) / subdirectory
        new_subdirectory_path.mkdir(parents=True, exist_ok=True)
