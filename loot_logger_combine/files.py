"""
TODO: Docstring
"""

import glob
import json
import os
import shutil
from pathlib import Path

from .models import FileMatch, FileNoMatch, Record


def find_files(path: Path, extension: str = ".log") -> set[str]:
    """Finds all files with a given extension in a given directory."""
    matches = glob.glob(str(path / Path(f"**/*{extension}")), recursive=True)
    return {os.path.relpath(Path(match), path) for match in matches}


def combine_files(
    match: FileMatch,
    output_directory: str,
    sort: bool = True,
) -> None:
    """"""  # TODO: Docstring
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


def copy_file(non_match: FileNoMatch, output_directory: str) -> None:
    """"""  # TODO: Docstring
    output_path = os.path.join(output_directory, non_match.relative)
    shutil.copy2(non_match.path(), output_path)
