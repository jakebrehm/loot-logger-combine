"""
Combines JSON Lines data from multiple files into a single file.

The source of these data files is the Loot Logger plugin from the RuneLite
Plugin Hub.
"""

from pathlib import Path

import typer

from loot_logger_combine.files import combine_files, copy_file, find_files
from loot_logger_combine.types import PathMap
from loot_logger_combine.utility import (
    combine_directory_structures,
    match_paths,
)

# MARK: CLI


app = typer.Typer()


# MARK: Main


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
