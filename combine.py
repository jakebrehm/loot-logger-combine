"""
Combines JSON Lines data from multiple files into a single file.

The source of these data files is the Loot Logger plugin from the RuneLite
Plugin Hub.
"""

import glob
import os
from pathlib import Path

import typer

from loot_logger_combine.files import combine_files, copy_file
from loot_logger_combine.models import FileMatch, FileNoMatch

# MARK: CLI


app = typer.Typer()


# MARK: Main


type PathMap = dict[str, set[str]]


def find_files(path: Path, extension: str = ".log") -> set[str]:
    """Finds all files with a given extension in a given directory."""
    matches = glob.glob(str(path / Path(f"**/*{extension}")), recursive=True)
    return {os.path.relpath(Path(match), path) for match in matches}


def match_paths(path_map: PathMap) -> tuple[list[FileMatch], list[FileNoMatch]]:
    """"""  # TODO: Docstring

    # Determine which files exist across all directories
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
    return result_matches, result_no_matches


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


def main(inputs: list[str], output: str) -> None:
    """The main function of the program."""

    # Find the files in each directory
    result: PathMap = {i: find_files(Path(i)) for i in inputs}
    matched, unmatched = match_paths(result)

    # Copy the structure of the folders in each directory
    combine_directory_structures(inputs, output)

    # Combine the files that match
    for item in matched:
        combine_files(item, output)

    # Copy the files that don't match
    for item in unmatched:
        copy_file(item, output)


if __name__ == "__main__":
    typer.run(main)
