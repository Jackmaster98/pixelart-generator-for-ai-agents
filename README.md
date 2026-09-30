# 🎨 PixelSpriteAI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**PixelSpriteAI** is a lightweight Python library designed specifically as an interface between LLM (Large Language Model) agents and a 2D graphics rendering engine. 

Instead of letting agents struggle with raw pixel matrices or complex image generation prompts, PixelSpriteAI allows them to generate pixel art deterministically through high-level geometric commands. It is optimized for token usage, robust error handling, and perfect crisp exports.

## ✨ Features

- 🤖 **Agent-Friendly Interface**: Exposes intuitive methods (`draw_pixel`, `draw_line`, `draw_rectangle`) that easily map to function calls for an LLM.
- 🎚️ **Free Resolution**: no fixed canvas size. The logical grid and the PNG output size are two independent choices, both adjustable at any time (`set_resolution`, `set_scale_factor`, per-export override, `export_exact`). Anisotropic `(x, y)` scaling is supported too.
- 🛡️ **Hallucination-Proof Error Handling**: Catches out-of-bounds coordinates and invalid colors without crashing. It returns textual warnings back to the agent so it can learn and correct its mistakes dynamically.
- 🔄 **Auto-Sorting Coordinates**: Automatically corrects inverted rectangle coordinates.
- 🔍 **Crisp Export**: Scales up pixel art cleanly using `NEAREST` resampling to maintain sharp, perfect edges without blurring.
- 🚀 **Antigravity Skill Ready**: Includes a `SKILL.md` to be instantly loaded as a behavior guideline by AI agents using the Antigravity platform.

## 📦 Installation

PixelSpriteAI requires Python 3.8+ and the `Pillow` library.

```bash
pip install Pillow
```

Make sure the `pixelspriteai` directory is in your Python path, or install it directly as a module.

## 🚀 Usage Example

This is a typical script an AI agent would write to generate a sprite:

```python
from pixelspriteai import SpriteCanvas

# Initialize a 16x16 transparent canvas with an export scale factor of 20
canvas = SpriteCanvas(width=16, height=16, scale_factor=20)

# Draw the base (main body)
canvas.draw_rectangle(2, 2, 14, 14, "red")

# Add outlines
canvas.draw_line(4, 4, 12, 12, "blue")

# Add fine details
canvas.draw_pixel(8, 8, "#00FF00")

# Export to a PNG file (will result in a crisp 320x320 image)
print(canvas.export("my_sprite.png"))
# Success: exported 'my_sprite.png' (16x16 grid at 20x -> 320x320 px).
```

### 🎚️ Choosing the resolution

Nothing forces you to 16x16: pick the grid that fits the asset, then decide how big the
PNG must be.

```python
# A wide banner on its own grid, exported 8x
SpriteCanvas(width=48, height=16, scale_factor=8)

# Need more room while drawing? Resize instead of starting over.
canvas.set_resolution(24, 24)          # keeps what you drew (topleft)
canvas.set_resolution(32, 32, anchor="center")

# Same drawing, two different outputs
canvas.export("hero.png")                       # uses the canvas factor
canvas.export("hero_4x.png", scale_factor=4)    # per-export override
canvas.export("hero_tall.png", scale_factor=(4, 6))

# Target an exact size (e.g. an atlas slot)
canvas.export_exact("hero_96.png", 96)          # warns if not an exact multiple

# What am I working with?
canvas.info()
# {'width': 32, 'height': 32, 'scale_factor': 20, 'output_size': (640, 640), ...}
```

## 🧠 Guidelines for AI Agents

If you are an LLM using this library, remember these core rules:
1. **Work in Layers**: Draw the largest forms first (`draw_rectangle`, `draw_line`) and finish with fine details (`draw_pixel`).
2. **Respect the Canvas**: The default canvas is completely transparent `(0, 0, 0, 0)`. Do not flood-fill the background.
3. **Choose the resolution deliberately**: draw coarse and export large — every extra pixel of grid costs you tool calls, magnification costs nothing.
4. **Handle Errors**: If a method returns a string starting with `"Warning:"`, read it, adjust your logic, and avoid repeating the mistake. You don't need to crash—just correct the next calls.

*(For detailed instructions, point your agent to read the `SKILL.md` file included in this repository).*

## 🧪 Testing

The library comes with a full test suite. You can run the tests using `pytest`:

```bash
pip install pytest
PYTHONPATH=. pytest tests/
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
