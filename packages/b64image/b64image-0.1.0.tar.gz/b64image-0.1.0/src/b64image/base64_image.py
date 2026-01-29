from __future__ import annotations

import os
import re
from base64 import b64decode, b64encode
from pathlib import Path
from typing import (
    Iterator,
    Literal,
    NamedTuple,
    Optional,
    Self,
    TypeAlias,
    get_args,
)
from urllib.parse import urlparse

from .imghdr import TestableImageType, what

ImageType: TypeAlias = Literal["jpeg", "png", "gif", "webp", "bmp"]
ALLOWED_IMAGE_FORMATS: tuple[ImageType, ...] = get_args(ImageType)
IMAGE_PATTERN = re.compile(
    r"data:image/("
    + "|".join(ALLOWED_IMAGE_FORMATS)
    + r");base64,([A-Za-z0-9+/]+={0,2})"
)


class Base64Image(NamedTuple):
    ext: ImageType
    data: str

    def __hash__(self) -> int:
        return hash((self.ext, self.data))

    # ===== Encoding (from various sources) =====

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        """Create Base64Image from raw image bytes."""
        maybe_supported_ext: TestableImageType | None = what(data)
        if maybe_supported_ext is None:
            raise ValueError("Cannot determine image type from bytes")
        supported_ext = _guess_image_extension(maybe_supported_ext)
        if supported_ext is None:
            raise ValueError(f"Unsupported image type: {maybe_supported_ext}")
        return cls(ext=supported_ext, data=b64encode(data).decode("ascii"))

    @classmethod
    def from_base64(cls, data: str) -> Self:
        """Create Base64Image from a base64 string (with or without data URI prefix)."""
        if match := IMAGE_PATTERN.fullmatch(data):
            if (maybe_ext := _guess_image_extension(match.group(1))) is None:
                raise ValueError("Invalid Image Format")
            return cls(ext=maybe_ext, data=match.group(2))
        if (maybe_ext := _guess_image_extension(what(data) or "")) is None:
            raise ValueError("Invalid Image Format")
        return cls(ext=maybe_ext, data=data)

    @classmethod
    def from_path(cls, path: os.PathLike[str] | str) -> Self:
        """Create Base64Image from a local file path."""
        if isinstance(path, str):
            path = _parse_path(path)
        else:
            path = Path(path)
        if path.is_file():
            return cls.from_bytes(path.read_bytes())
        else:
            raise FileNotFoundError(f"File not found: {path}")

    @classmethod
    def from_url(cls, url: str, *, timeout: float = 30.0) -> Self:
        """Create Base64Image from a remote URL (HTTP/HTTPS)."""
        import urllib.request

        if not _is_remote_url(url):
            raise ValueError(f"Invalid URL: {url}")

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; b64image/1.0)",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
            if not isinstance(data, bytes):
                raise ValueError("Failed to read image data from URL")
            return cls.from_bytes(data)

    @classmethod
    def from_auto(cls, source: str) -> Self:
        """Automatically detect source type and create Base64Image.

        Supports:
        - Local file paths
        - file:// URIs
        - HTTP/HTTPS URLs
        - Data URIs
        - Raw base64 strings
        """
        # Data URI
        if source.startswith("data:image/"):
            return cls.from_base64(source)

        # Remote URL
        if _is_remote_url(source):
            return cls.from_url(source)

        # File URI or local path
        return cls.from_path(source)

    # ===== Decoding (to various outputs) =====

    def to_bytes(self) -> bytes:
        """Decode base64 data to raw bytes."""
        return b64decode(self.data)

    def save(self, path: os.PathLike[str] | str) -> Path:
        """Save decoded image to a file."""
        if isinstance(path, str):
            path = Path(path)
        else:
            path = Path(path)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.to_bytes())
        return path

    # ===== Properties =====

    @property
    def data_uri(self) -> str:
        """Return data URI string."""
        return f"data:image/{self.ext};base64,{self.data}"

    @property
    def size_bytes(self) -> int:
        """Return the size of decoded image in bytes."""
        return len(self.to_bytes())


# ===== Batch Processing =====


def load_images(
    sources: list[str],
    *,
    skip_errors: bool = False,
) -> Iterator[Base64Image]:
    """Load multiple images from various sources.

    Args:
        sources: List of file paths, URLs, or base64 strings
        skip_errors: If True, skip failed images instead of raising

    Yields:
        Base64Image objects
    """
    for source in sources:
        try:
            img = Base64Image.from_auto(source)
            yield img
        except Exception as e:
            if skip_errors:
                continue
            raise ValueError(f"Failed to load image from {source}: {e}") from e


def load_images_from_directory(
    directory: os.PathLike[str] | str,
    *,
    pattern: str = "*",
    recursive: bool = False,
    extensions: tuple[str, ...] = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"),
    skip_errors: bool = False,
) -> Iterator[Base64Image]:
    """Load all images from a directory.

    Args:
        directory: Directory path
        pattern: Glob pattern for matching files
        recursive: If True, search recursively
        extensions: File extensions to include
        skip_errors: If True, skip failed images

    Yields:
        Base64Image objects
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    glob_method = dir_path.rglob if recursive else dir_path.glob

    for file_path in glob_method(pattern):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                yield Base64Image.from_path(file_path)
            except Exception:
                if not skip_errors:
                    raise


# ===== Helper Functions =====


def _is_remote_url(path: str) -> bool:
    parsed = urlparse(path)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def _guess_image_extension(ext: str) -> Optional[ImageType]:
    lowered: str = ext.lower().removeprefix(".")
    if lowered in ALLOWED_IMAGE_FORMATS:
        return lowered  # type: ignore[return-value]
    elif lowered == "jpg":
        return "jpeg"
    return None


def _parse_path(path_string: str) -> Path:
    """Convert a path string to a platform-specific Path object."""

    if not path_string:
        path_string = "."

    # Convert file:// URI to a platform-specific path
    if path_string.startswith("file://"):
        parsed = urlparse(path_string)

        # Ignore localhost
        netloc = parsed.netloc
        if netloc == "localhost":
            netloc = ""

        if netloc:
            # Check if netloc is a drive letter (C:, D:, etc.)
            if len(netloc) == 2 and netloc[1] == ":":
                # file://C:/Users -> C:/Users
                path_string = f"{netloc}{parsed.path}"
            else:
                # file://server/share -> //server/share (UNC)
                path_string = f"//{netloc}{parsed.path}"
        else:
            # file:///path or file://localhost/path
            path_string = parsed.path
            # file:///C:/... -> C:/...
            if len(path_string) > 2 and path_string[0] == "/" and path_string[2] == ":":
                path_string = path_string[1:]

    # Normalize backslashes to forward slashes
    path_string = path_string.replace("\\", "/")

    # /C:/... -> C:/...
    if len(path_string) > 2 and path_string[0] == "/" and path_string[2] == ":":
        path_string = path_string[1:]

    return Path(path_string)
