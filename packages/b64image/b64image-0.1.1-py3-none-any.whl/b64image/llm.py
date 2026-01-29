"""LLM API integration helpers for various providers."""

from __future__ import annotations

from typing import Literal, TypedDict

from .base64_image import Base64Image

LLMProvider = Literal["openai", "anthropic", "google", "generic"]


class OpenAIImageContent(TypedDict):
    """OpenAI vision API image content block."""

    type: Literal["image_url"]
    image_url: dict[str, str]


class AnthropicImageContent(TypedDict):
    """Anthropic Claude vision API image content block."""

    type: Literal["image"]
    source: dict[str, str]


class GoogleImageContent(TypedDict):
    """Google Gemini vision API image content block."""

    inline_data: dict[str, str]


def to_openai(image: Base64Image) -> OpenAIImageContent:
    """Convert Base64Image to OpenAI vision API format.

    Usage:
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                to_openai(img),
            ]
        }
    """
    return {
        "type": "image_url",
        "image_url": {"url": image.data_uri},
    }


def to_anthropic(image: Base64Image) -> AnthropicImageContent:
    """Convert Base64Image to Anthropic Claude vision API format.

    Usage:
        message = {
            "role": "user",
            "content": [
                to_anthropic(img),
                {"type": "text", "text": "What's in this image?"},
            ]
        }
    """
    media_type = f"image/{image.ext}"
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": image.data,
        },
    }


def to_google(image: Base64Image) -> GoogleImageContent:
    """Convert Base64Image to Google Gemini vision API format.

    Usage:
        content = [
            to_google(img),
            "What's in this image?",
        ]
    """
    return {
        "inline_data": {
            "mime_type": f"image/{image.ext}",
            "data": image.data,
        }
    }


def to_llm(
    image: Base64Image,
    provider: LLMProvider = "openai",
) -> OpenAIImageContent | AnthropicImageContent | GoogleImageContent:
    """Convert Base64Image to the specified LLM provider's format.

    Args:
        image: Base64Image to convert
        provider: Target LLM provider ("openai", "anthropic", "google", "generic")

    Returns:
        Provider-specific image content block
    """
    if provider == "openai" or provider == "generic":
        return to_openai(image)
    elif provider == "anthropic":
        return to_anthropic(image)
    elif provider == "google":
        return to_google(image)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def create_message_content(
    *contents: str | Base64Image,
    provider: LLMProvider = "openai",
) -> list[dict[str, object]]:
    """Create message content for the specified provider.

    Args:
        *contents: Text strings and Base64Image objects in any order
        provider: Target LLM provider

    Returns:
        List of content blocks ready for API call

    Example:
        >>> img = Base64Image.from_path("photo.jpg")
        >>> content = create_message_content("Describe this:", img)
        >>> content = create_message_content(img, "What's in this image?")
        >>> content = create_message_content("Image 1:", img1, "Image 2:", img2, "Compare them.")
        >>> message = {"role": "user", "content": content}
    """
    result: list[dict[str, object]] = []

    for item in contents:
        if isinstance(item, str):
            if provider == "google":
                result.append({"text": item})
            else:
                result.append({"type": "text", "text": item})
        else:
            if provider == "google":
                result.append(dict(to_google(item)))
            elif provider == "anthropic":
                result.append(dict(to_anthropic(item)))
            else:
                result.append(dict(to_openai(item)))

    return result


def batch_to_llm(
    images: list[Base64Image],
    provider: LLMProvider = "openai",
) -> list[OpenAIImageContent | AnthropicImageContent | GoogleImageContent]:
    """Convert multiple images to LLM format.

    Args:
        images: List of Base64Image objects
        provider: Target LLM provider

    Returns:
        List of provider-specific image content blocks
    """
    return [to_llm(img, provider) for img in images]
