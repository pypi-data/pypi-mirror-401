"""Command-line interface for b64image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .base64_image import Base64Image, load_images_from_directory
from .llm import LLMProvider, to_llm


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="b64image",
        description="Encode images to base64 and decode base64 to images",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # encode command
    encode_parser = subparsers.add_parser(
        "encode",
        help="Encode image(s) to base64",
    )
    encode_parser.add_argument(
        "source",
        nargs="+",
        help="Image source(s): file path, URL, or directory",
    )
    encode_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file (default: stdout)",
    )
    encode_parser.add_argument(
        "--format",
        choices=["raw", "data-uri", "json"],
        default="data-uri",
        help="Output format (default: data-uri)",
    )
    encode_parser.add_argument(
        "--llm",
        choices=["openai", "anthropic", "google"],
        help="Output in LLM provider format (JSON)",
    )
    encode_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Search directories recursively",
    )

    # decode command
    decode_parser = subparsers.add_parser(
        "decode",
        help="Decode base64 to image file",
    )
    decode_parser.add_argument(
        "input",
        help="Base64 string, data URI, or file containing base64",
    )
    decode_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output image file path",
    )

    # info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show image information",
    )
    info_parser.add_argument(
        "source",
        help="Image source: file path, URL, or base64 string",
    )

    args = parser.parse_args()

    try:
        if args.command == "encode":
            return cmd_encode(args)
        elif args.command == "decode":
            return cmd_decode(args)
        elif args.command == "info":
            return cmd_info(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_encode(args: argparse.Namespace) -> int:
    """Handle encode command."""
    import json

    # Collect all image sources
    sources: list[str] = []
    for source in args.source:
        source_path = Path(source)
        if source_path.is_dir():
            extensions = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
            glob_method = source_path.rglob if args.recursive else source_path.glob
            for file_path in glob_method("*"):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    sources.append(str(file_path))
        else:
            sources.append(source)

    if not sources:
        print("No images found", file=sys.stderr)
        return 1

    # Load images
    images: list[Base64Image] = []
    for source in sources:
        try:
            img = Base64Image.from_auto(source)
            images.append(img)
        except Exception as e:
            print(f"Warning: Failed to load {source}: {e}", file=sys.stderr)

    if not images:
        print("No images could be loaded", file=sys.stderr)
        return 1

    # Format output
    output_lines: list[str] = []

    for img in images:
        if args.llm:
            provider: LLMProvider = args.llm
            output_lines.append(json.dumps(to_llm(img, provider), indent=2))
        elif args.format == "raw":
            output_lines.append(img.data)
        elif args.format == "data-uri":
            output_lines.append(img.data_uri)
        elif args.format == "json":
            output_lines.append(
                json.dumps(
                    {
                        "ext": img.ext,
                        "data": img.data,
                        "data_uri": img.data_uri,
                    },
                    indent=2,
                )
            )

    output = "\n".join(output_lines)

    if args.output:
        args.output.write_text(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


def cmd_decode(args: argparse.Namespace) -> int:
    """Handle decode command."""
    input_str = args.input

    # Check if input is a file
    input_path = Path(input_str)
    if input_path.is_file():
        input_str = input_path.read_text().strip()

    # Parse and decode
    img = Base64Image.from_base64(input_str)
    saved_path = img.save(args.output)
    print(f"Saved to {saved_path}")

    return 0


def cmd_info(args: argparse.Namespace) -> int:
    """Handle info command."""
    source = args.source

    # Try to determine source type and load
    if source.startswith("data:image/"):
        img = Base64Image.from_base64(source)
        source_type = "data URI"
    elif Path(source).is_file():
        img = Base64Image.from_path(source)
        source_type = "file"
    elif source.startswith(("http://", "https://")):
        img = Base64Image.from_url(source)
        source_type = "URL"
    else:
        # Try as base64
        img = Base64Image.from_base64(source)
        source_type = "base64"

    print(f"Source: {source_type}")
    print(f"Format: {img.ext}")
    print(f"Size: {img.size_bytes:,} bytes")
    print(f"Base64 length: {len(img.data):,} characters")

    return 0


# Keep for backwards compatibility
__all__ = ["main", "load_images_from_directory"]

if __name__ == "__main__":
    sys.exit(main())
