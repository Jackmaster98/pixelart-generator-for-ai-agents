# PixelSpriteAI

PixelSpriteAI is a Python library that serves as an interface (wrapper) between an LLM agent and a graphics rendering engine. It enables agents to generate 2D pixel art (sprites with transparency) deterministically, optimizing token usage through high-level geometric commands rather than pixel matrices.

## Features

- **Agent-Friendly Interface:** Exposes methods like `draw_pixel`, `draw_line`, and `draw_rectangle` that can easily be mapped to function calls for an LLM.
- **Robust Error Handling:** Designed to be "hallucination-proof". It catches out-of-bounds coordinates and invalid colors without crashing, returning textual warnings back to the agent instead.
- **Auto-Sorting Coordinates:** Automatically corrects inverted rectangle coordinates.
- **Crisp Export:** Scales up pixel art cleanly using `NEAREST` resampling to maintain sharp edges.

## Requirements

- Python 3.8+
- `Pillow` (PIL Fork)

## Installation

```bash
pip install Pillow
```

Make sure the `pixelspriteai` directory is in your Python path or package it as a module.

## Usage Example

```python
from pixelspriteai import SpriteCanvas

# Initialize a 16x16 transparent canvas with an export scale factor of 10
canvas = SpriteCanvas(width=16, height=16, scale_factor=10)

# Draw a red rectangle
canvas.draw_rectangle(2, 2, 14, 14, "red")

# Draw a blue line
canvas.draw_line(4, 4, 12, 12, "blue")

# Draw a single green pixel
canvas.draw_pixel(8, 8, "#00FF00")

# Export to a PNG file (will be 160x160 pixels due to the scale_factor)
canvas.export("my_sprite.png")
```

## Testing

You can run the tests using `pytest`:

```bash
pip install pytest
PYTHONPATH=. pytest tests/
```
