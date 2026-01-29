# b64image

Base64 image encoding/decoding with LLM API support.

## Installation

```bash
uv add b64image
```

## Usage

### Python API

```python
from b64image import Base64Image, to_openai, to_anthropic, create_vision_message

# Load from various sources
img = Base64Image.from_path("photo.png")
img = Base64Image.from_url("https://example.com/image.jpg")
img = Base64Image.from_bytes(raw_bytes)
img = Base64Image.from_base64("iVBORw0KGgo...")
img = Base64Image.from_auto("photo.png")  # auto-detect source type

# Convert to outputs
img.to_bytes()        # raw bytes
img.save("output.png") # save to file
img.data_uri          # data:image/png;base64,...

# LLM API formats
to_openai(img)     # OpenAI vision format
to_anthropic(img)  # Anthropic Claude format
to_google(img)     # Google Gemini format

# Create complete vision message
msg = create_vision_message(
    "What's in this image?",
    [img],
    provider="openai"  # or "anthropic", "google"
)
```

### Batch Processing

```python
from b64image import load_images, load_images_from_directory

# Load multiple images
for img in load_images(["a.png", "b.jpg", "https://example.com/c.webp"]):
    print(img.ext, img.size_bytes)

# Load from directory
for img in load_images_from_directory("./images", recursive=True):
    print(img.data_uri)
```

### CLI

```bash
# Encode image to base64
b64image encode photo.png
b64image encode photo.png --format raw
b64image encode photo.png --llm openai

# Encode directory
b64image encode ./images/ -r

# Decode base64 to file
b64image decode "data:image/png;base64,..." -o output.png

# Show image info
b64image info photo.png
```

## Supported Formats

JPEG, PNG, GIF, WebP, BMP
