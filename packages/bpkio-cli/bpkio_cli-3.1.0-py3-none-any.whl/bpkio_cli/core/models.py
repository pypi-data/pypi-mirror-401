"""CLI-specific models for resource tracking."""

from pathlib import PosixPath
from typing import Union

from pydantic import BaseModel, Field, field_validator


class Archive(BaseModel):
    """Represents a trace/archive file path as a typed resource.

    This model is used to store archive paths in the resource cache and chain,
    providing type safety and consistent handling of trace files.
    """

    path: Union[PosixPath, str] = Field(..., description="The path to the trace/archive file or directory")

    @field_validator("path", mode="before")
    @classmethod
    def validate_path(cls, v):
        """Convert string paths to PosixPath for consistency."""
        if isinstance(v, str):
            return PosixPath(v)
        return v

    @property
    def id(self) -> str:
        """Return the path as a string for use as an ID."""
        return str(self.path)

    @property
    def summary(self) -> str:
        """Return a summary string for display."""
        return f"{self.path}"

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.path)

    def __repr__(self) -> str:
        """Return representation."""
        return f"Archive(path={self.path!r})"

    def to_posix_path(self) -> PosixPath:
        """Convert to PosixPath object."""
        if isinstance(self.path, PosixPath):
            return self.path
        return PosixPath(self.path)

    @classmethod
    def from_posix_path(cls, path: PosixPath) -> "Archive":
        """Create Archive from PosixPath."""
        return cls(path=path)

