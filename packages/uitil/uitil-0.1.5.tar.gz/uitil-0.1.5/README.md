# uitil

Simple utility functions for common image operations.

## Installation

```bash
pip install uitil
```

## Usage

```python
from uitil import set, get

# Embed text in an image
set('input.png', 'your data here', 'output.png')

# Extract text from an image
data = get('output.png')
print(data)
```

## Functions

### set(image_path, data, output_path=None)

Embeds text data into an image file.

**Parameters:**
- `image_path` (str): Path to input image
- `data` (str): Text to embed in the image
- `output_path` (str, optional): Output path (default: adds '_out' to filename)

**Returns:**
- str: Path to the output image

### get(image_path)

Extracts embedded data from an image file.

**Parameters:**
- `image_path` (str): Path to image containing data

**Returns:**
- str: The extracted text

## Example

```python
from uitil import set, get

# Embed a message
output = set('photo.png', 'Hello World', 'secret.png')
print(f"Created: {output}")

# Extract the message
message = get('secret.png')
print(f"Message: {message}")
```

## Requirements

- Python 3.6+
- Pillow

## License

MIT