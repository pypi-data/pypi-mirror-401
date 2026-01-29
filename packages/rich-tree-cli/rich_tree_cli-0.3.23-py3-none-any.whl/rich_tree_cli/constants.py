"""RichTreeCLI constants and data classes."""

from __future__ import annotations

from enum import IntEnum
from importlib.metadata import version
from pathlib import Path
from typing import Any, Final, Literal, Self

CONFIG_PATH: Final[Path] = Path.home() / ".config" / "rich_tree_cli" / "config.toml"

type SortChoice = Literal["files", "dirs", "size", "modified", "created"]
SORT_CHOICES: Final[list[str]] = ["files", "dirs", "size", "modified", "created"]

type IconChoice = Literal["plain", "emoji", "glyphs"]
ICON_CHOICES: Final[list[str]] = ["plain", "emoji", "glyphs"]

type MetaDataChoice = Literal["none", "size", "lines", "created", "modified", "all"]
METADATA_CHOICES: Final[list[str]] = ["none", "size", "lines", "created", "modified", "all"]
ALL_METADATA: Final[list[str]] = ["size", "lines", "created", "modified"]

DEFAULT_FMT: Final[list[str]] = ["text"]

EMPTY_LIST: Final[list[Any]] = []
type TomlData = dict[str, dict[str, Any]]


EXT_MAP: dict[OutputFormat, str] = {}


class OutputFormat(IntEnum):
    """Enum for output formats."""

    TEXT = 0
    MARKDOWN = 1
    HTML = 2
    JSON = 3
    SVG = 4
    TOML = 5
    XML = 6

    @classmethod
    def to_ext(cls, name: str, default: str = ".txt", ext_map: dict[OutputFormat, str] = EXT_MAP) -> str:
        """Get the file extension for the output format."""
        return ext_map.get(cls.key_to_fmt(name), default)

    @classmethod
    def key_to_fmt(cls, key: str) -> Self:
        """Get the value of the enum based on the key."""
        try:
            return cls[key.upper()]
        except KeyError:
            raise ValueError(f"Invalid output format key: {key}") from None

    @classmethod
    def choices(cls) -> list[str]:
        """Return a list of available output format choices."""
        return [format.name.lower() for format in cls]

    @classmethod
    def default(cls) -> list[str]:
        """Return the default output format."""
        default: Literal[OutputFormat.TEXT] = OutputFormat.TEXT

        return [default.name.lower()]


for format_enum, extension in [
    (OutputFormat.TEXT, "txt"),
    (OutputFormat.MARKDOWN, "md"),
    (OutputFormat.HTML, "html"),
    (OutputFormat.JSON, "json"),
    (OutputFormat.SVG, "svg"),
    (OutputFormat.TOML, "toml"),
    (OutputFormat.XML, "xml"),
]:
    EXT_MAP[format_enum] = extension


__version__: str = version("rich-tree-cli")
