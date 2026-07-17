# 🎨 PixelSpriteAI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**PixelSpriteAI** is a lightweight Python library designed specifically as an interface between LLM (Large Language Model) agents and a 2D graphics rendering engine. 

Instead of letting agents struggle with raw pixel matrices or complex image generation prompts, PixelSpriteAI allows them to generate pixel art deterministically through high-level geometric commands. It is optimized for token usage, robust error handling, and perfect crisp exports.

## ✨ Features

- 🤖 **Agent-Friendly Interface**: Exposes intuitive methods (`draw_pixel`, `draw_line`, `draw_rectangle`) that easily map to function calls for an LLM.
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
canvas.export("my_sprite.png")
```

## 🧠 Guidelines for AI Agents

If you are an LLM using this library, remember these core rules:
1. **Work in Layers**: Draw the largest forms first (`draw_rectangle`, `draw_line`) and finish with fine details (`draw_pixel`).
2. **Respect the Canvas**: The default canvas is completely transparent `(0, 0, 0, 0)`. Do not flood-fill the background.
3. **Handle Errors**: If a method returns a string starting with `"Warning:"`, read it, adjust your logic, and avoid repeating the mistake. You don't need to crash—just correct the next calls.

*(For detailed instructions, point your agent to read the `SKILL.md` file included in this repository).*

## 🧪 Testing

The library comes with a full test suite. You can run the tests using `pytest`:

```bash
pip install pytest
PYTHONPATH=. pytest tests/
```

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
