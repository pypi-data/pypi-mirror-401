"""b64image - Base64 image encoding/decoding with LLM API support."""

from .base64_image import (
    ALLOWED_IMAGE_FORMATS,
    Base64Image,
    ImageType,
    load_images,
    load_images_from_directory,
)
from .imghdr import what
from .llm import (
    LLMProvider,
    batch_to_llm,
    create_message_content,
    to_anthropic,
    to_google,
    to_llm,
    to_openai,
)

__all__ = [
    # Core
    "Base64Image",
    "ImageType",
    "ALLOWED_IMAGE_FORMATS",
    # Batch
    "load_images",
    "load_images_from_directory",
    # Image detection
    "what",
    # LLM helpers
    "LLMProvider",
    "to_openai",
    "to_anthropic",
    "to_google",
    "to_llm",
    "batch_to_llm",
    "create_message_content",
]
