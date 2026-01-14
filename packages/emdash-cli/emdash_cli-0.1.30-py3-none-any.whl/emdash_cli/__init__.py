"""EmDash CLI - Command-line interface for code intelligence."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("emdash-cli")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
