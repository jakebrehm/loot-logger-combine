"""
TODO: Docstring
"""

import datetime as dt
import json
import os
from dataclasses import dataclass, field

# MARK: Types


type RecordJSON = dict


# MARK: Models


@dataclass
class FileMatch:
    """"""  # TODO: Docstring

    bases: list[str]
    relative: str

    def __post_init__(self):
        """Performs operations after initialization."""
        assert self.bases, "base must not be empty"

    def paths(self) -> list[str]:
        """"""  # TODO: Docstring
        return [os.path.join(base, self.relative) for base in self.bases]


@dataclass
class FileNoMatch:
    """"""  # TODO: Docstring

    base: str
    relative: str

    def path(self) -> str:
        """"""  # TODO: Docstring
        return os.path.join(self.base, self.relative)


@dataclass
class Record:
    """"""  # TODO: Docstring

    name: str
    level: int
    kill_count: int
    type_: str
    drops: list[dict] = field(repr=False)
    date: dt.datetime

    @classmethod
    def from_json(cls, data: RecordJSON):
        return cls(
            name=data["name"],
            level=data["level"],
            kill_count=data["killCount"],
            type_=data["type"],
            drops=data["drops"],
            date=dt.datetime.strptime(data["date"], r"%b %d, %Y, %I:%M:%S %p"),
        )

    def to_json(self) -> RecordJSON:
        return {
            "name": self.name,
            "level": self.level,
            "killCount": self.kill_count,
            "type": self.type_,
            "drops": self.drops,
            "date": self.date.strftime(r"%b %-d, %Y, %-I:%M:%S %p"),
        }

    def to_json_line(self) -> str:
        return json.dumps(self.to_json())
