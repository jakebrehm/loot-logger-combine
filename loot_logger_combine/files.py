"""
Contains functions for working with files and the file system.
"""

import glob
import json
import os
import shutil
from pathlib import Path

from .models import Match, Record


def find_files(path: Path, extension: str = ".log") -> set[str]:
    """Finds all files with a given extension in a given directory."""
    matches = glob.glob(str(path / Path(f"**/*{extension}")), recursive=True)
    return {os.path.relpath(Path(match), path) for match in matches}


def combine_files(
    match: Match, output_directory: str, sort: bool = True
) -> None:
    """Combines matched files into a single file in the output directory."""
    records: list[Record] = []
    for path in match.paths():
        with open(path, "r") as file:
            for line in file.readlines():
                record = Record.from_json(json.loads(line))
                records.append(record)
    if sort:
        records.sort(key=lambda record: record.date)
    with open(os.path.join(output_directory, match.relative), "w") as file:
        file.write("\n".join([record.to_json_line() for record in records]))


def copy_file(match: Match, output_directory: str) -> None:
    """Copies an unmatched file to the output directory."""
    output_path = os.path.join(output_directory, match.relative)
    shutil.copy2(match.paths()[0], output_path)
