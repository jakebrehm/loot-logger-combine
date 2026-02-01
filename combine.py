"""
Combines JSON Lines data from multiple files into a single file.

The source of these data files is the Loot Logger plugin from the RuneLite
Plugin Hub.
"""

from pathlib import Path
from typing import Annotated

import typer
from typer import Argument, Option

from loot_logger_combine.files import combine_files, copy_file, find_files
from loot_logger_combine.types import PathMap
from loot_logger_combine.utility import (
    combine_directory_structures,
    match_paths,
)

# MARK: CLI


app = typer.Typer()


# MARK: Main


def main(
    inputs: Annotated[list[str], Argument(help="Input directories.")],
    output: Annotated[str, Option("-o", "--output", help="Output directory.")],
) -> None:
    """The main function of the program."""

    # Find the files in each directory
    path_map: PathMap = {i: find_files(Path(i)) for i in inputs}
    matches = match_paths(path_map)

    # Copy the structure of the folders in each directory
    combine_directory_structures(inputs, output)

    # Copy or combine the files
    for match in matches:
        function = combine_files if len(match.bases) > 1 else copy_file
        function(match, output)


if __name__ == "__main__":
    typer.run(main)
