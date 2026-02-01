"""
Contains utility functions used across the package.
"""

import os
from pathlib import Path

from .models import FileMatch, FileNoMatch
from .types import PathMap

# MARK: Functions


def match_paths(path_map: PathMap) -> tuple[list[FileMatch], list[FileNoMatch]]:
    """Determines which files match or don't match across directories."""

    # TODO: This function can be made much more efficient, but it works

    # Find full matches (files that exist in all directories)
    matched_paths: set[str] = set.intersection(*path_map.values())
    result_matches: list[FileMatch] = [
        FileMatch(list(path_map.keys()), path) for path in matched_paths
    ]

    # Determine which files don't exist across all directories
    result_no_matches: list[FileNoMatch] = []
    for base_path, relative_paths in path_map.items():
        for relative_path in relative_paths:
            if relative_path in matched_paths:
                continue
            result_no_matches.append(FileNoMatch(base_path, relative_path))

    # Correct files that exist in multiple but not all directories
    new_matches: list[FileMatch] = result_matches.copy()
    new_no_matches: list[FileNoMatch] = []
    temporary: dict[str, list[FileNoMatch]] = {}
    for match in result_no_matches:
        temporary.setdefault(match.relative, []).append(match)

    for relative_path, matches in temporary.items():
        if len(matches) > 1:
            new_match = FileMatch(
                [match.base for match in matches], relative_path
            )
            new_matches.append(new_match)
        else:
            new_no_matches.append(matches[0])

    return new_matches, new_no_matches


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
