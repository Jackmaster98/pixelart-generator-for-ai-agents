# Guidelines for LLM Agents using PixelSpriteAI

This document provides system guidelines on how to effectively use the `PixelSpriteAI` library. If you are an AI model tasked with generating pixel art using this tool, follow these rules:

## 1. Work in Layers
Always draw the largest forms first to establish the base shape.
- Use `draw_rectangle` for the main body or background elements.
- Use `draw_line` for edges, limbs, or borders.
- Finally, use `draw_pixel` to add fine details like eyes, shading, or highlights.

## 2. Respect the Canvas
- **Do not fill the background.** The canvas is entirely transparent `(0, 0, 0, 0)` by default. If you don't draw on a pixel, it remains transparent.
- Be mindful of the canvas boundaries. The top-left corner is `(0, 0)`. The bottom-right corner is `(width-1, height-1)`. If you draw outside these bounds, your commands will be safely ignored or clamped, but it wastes your tokens.

## 3. Colors
- Use standard English color names (e.g., `"red"`, `"blue"`, `"black"`) or standard hexadecimal color codes (e.g., `"#FF5733"`).
- If you provide an invalid color, the system will use a shocking magenta (`#FF00FF`) as a fallback to highlight your error, and return a warning string.

## 4. Reading Feedback
- Most commands return `"Success"`.
- If a command returns a string starting with `"Warning:"` (e.g., an out-of-bounds coordinate or an invalid color), read the warning, adjust your logic, and avoid repeating the mistake. You do not need to crash or stop; just correct your next calls.

## 5. Available Tools
- `draw_pixel(x, y, color)`: Sets a single pixel.
- `draw_line(x1, y1, x2, y2, color)`: Draws a line between two points.
- `draw_rectangle(x1, y1, x2, y2, color)`: Draws and fills a rectangle. (Do not worry about the order of `x1, y1` vs `x2, y2`, they are auto-sorted).
- `erase_pixel(x, y)`: Makes a pixel fully transparent again.
- `clear_canvas()`: Erases everything on the canvas.
