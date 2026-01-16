# markdown-readtime

A library to estimate reading time for Markdown content with support for Chinese and English texts.

## Features

- 📊 Accurate estimation of Markdown text reading time
- 🌍 Support for both Chinese and English texts
- 😊 Emoji processing support
- 🖼️ Image reading time calculation
- 💻 Code block reading time calculation
- ⚙️ Customizable reading speed parameters
- 📦 Lightweight, zero dependencies (optional serde support)

## Installation

```bash
pip install markdown-readtime
```

## Usage

### Basic Usage

```python
from markdown_readtime import estimate, minutes, words, formatted

markdown_content = """
# My First Blog Post

This is some sample content to demonstrate how to use the markdown-readtime library.

## Subtitle

We can also add some lists:
- First item
- Second item
- Third item
"""

# Get full reading time information
read_time = estimate(markdown_content)
print(f"Total reading time: {read_time.total_seconds} seconds")
print(f"Formatted time: {read_time.formatted}")
print(f"Word count: {read_time.word_count}")

# Or use shortcut functions
print(f"Approximately {minutes(markdown_content)} minutes to read")
print(f"About {words(markdown_content)} words")
print(f"Reading time: {formatted(markdown_content)}")
```

### Custom Reading Speed

```python
from markdown_readtime import estimate_with_speed, ReadSpeed

markdown_content = "# Sample Article\n\nThis is test content for reading."

# Create custom reading speed configuration
speed = ReadSpeed(200, 15, 25, True, True)  # wpm, seconds_per_image, seconds_per_code_block, count_emoji, chinese
read_time = estimate_with_speed(markdown_content, speed)
print(f"Custom reading time: {read_time.total_seconds} seconds")
```

## API

### Classes

- `ReadTime`: Reading time estimation result
  - `total_seconds`: Total reading time in seconds
  - `formatted`: Formatted reading time string
  - `word_count`: Word count
  - `image_count`: Number of images
  - `code_block_count`: Number of code blocks

- `ReadSpeed`: Reading speed configuration
  - `words_per_minute`: Words per minute (default: 200)
  - `seconds_per_image`: Extra time per image in seconds (default: 12)
  - `seconds_per_code_block`: Extra time per code block in seconds (default: 20)
  - `count_emoji`: Whether to count emojis (default: True)
  - `chinese`: Whether text is Chinese (default: True)

### Functions

- `estimate(markdown: str) -> ReadTime`: Estimate reading time with default speed settings
- `estimate_with_speed(markdown: str, speed: ReadSpeed) -> ReadTime`: Estimate reading time with custom speed settings
- `minutes(markdown: str) -> int`: Get reading time in minutes (rounded up)
- `words(markdown: str) -> int`: Get word count
- `formatted(markdown: str) -> str`: Get formatted reading time string

## Building from Source

To build this package from source:

```bash
# Install maturin if you haven't already
pip install maturin

# Build the package
maturin develop  # For development
# or
maturin build    # To create a wheel
```

## License

This project is licensed under the MIT License.