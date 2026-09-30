---
name: pixel-sprite-ai
description: Genera pixel art con la libreria Python PixelSpriteAI.
disable-model-invocation: true
---

# Guidelines for LLM Agents using PixelSpriteAI

This document provides system guidelines on how to effectively use the `PixelSpriteAI` library. If you are an AI model tasked with generating pixel art using this tool, follow these rules.

## 0. You choose the resolution

There is **no fixed or recommended canvas size**: width, height and export size are entirely up to you,
and you may change your mind at any time. Decide them from the asset's *purpose* (a UI icon,
a character sprite, a tile, a sprite-sheet frame) rather than from habit.

- `width` and `height` are independent: **rectangular canvases are allowed**. The only hard limits are
  `1x1` minimum and `MAX_LOGICAL_SIZE` (1024) per side; anything bigger raises a clear `ValueError`.
- `scale_factor` (default `20`) decides **how big the PNG comes out**, not how detailed it is.
  It can be set at construction, changed later with `set_scale_factor()`, or overridden per export.
  It may also be a `(x, y)` tuple when you need a different horizontal/vertical magnification.
- Need a specific output? `export_exact("hero.png", 96)` targets an exact pixel size (handy for
  atlases and sprite sheets) and warns if your grid isn't divisible by an integer factor.
- Realised mid-drawing that you need more room? **`set_resolution(w, h)` keeps what you already drew**
  instead of forcing you to redraw everything (saves you a lot of tool calls).
- Not sure where you stand? `canvas.info()` returns grid size, scale factor and resulting output size.

**Choosing well — rough reference, adapt freely:**

| Asset | Typical grid | Note |
|---|---|---|
| Icona UI / piccolo pick-up | 8×8 – 16×16 | Readable at 1x, no doubt |
| Personaggio / unità | 16×16 – 32×32 | Enough face + silhouette |
| Tile ambientale | 16×16 – 24×24 | Must tile seamlessly |
| Oggetto grande / boss | 48×48 – 96×96 | Watch your token budget |
| Frame per animazione | same size as the base | One canvas per frame, then pack |

Two practical rules:
1. **Draw coarse, export large.** Detail costs tool calls (read: tokens); magnification is free. If unsure, start small and grow with `set_resolution`.
2. **Prefer sizes divisible by 4/8/16** when the destination is a sprite sheet or a game engine atlas: they pack cleanly and stay sharp at 2x/4x.

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
- If a command returns a string starting with `"Warning:"` (e.g., an out-of-bounds coordinate or an invalid color), read it, adjust your logic, and avoid repeating the mistake. You do not need to crash or stop; just correct your next calls.
- `export()` and `export_exact()` return a short report with the resulting image size: use it to confirm you actually got the resolution you wanted.

## 5. Available Tools
- `SpriteCanvas(width, height, scale_factor=20)`: Creates a new transparent canvas of the given `width` and `height`. `scale_factor` controls the export magnification.
- `set_resolution(width, height, anchor="topleft")`: Resizes the grid keeping the drawings (`anchor`: `topleft`, `center`, `bottomleft`).
- `set_scale_factor(scale_factor)`: Changes the default export magnification (int or `(x, y)` tuple).
- `info()`: Returns a dict with logical size, scale factor and resulting output size.
- `draw_pixel(x, y, color)`: Sets a single pixel.
- `draw_line(x1, y1, x2, y2, color)`: Draws a line between two points.
- `draw_rectangle(x1, y1, x2, y2, color)`: Draws and fills a rectangle. (Do not worry about the order of `x1, y1` vs `x2, y2`, they are auto-sorted).
- `erase_pixel(x, y)`: Makes a pixel fully transparent again.
- `clear_canvas()`: Erases everything on the canvas.
- `export(filename, scale_factor=None)`: Saves the canvas as a PNG scaled by the given factor (default: the canvas one) using `NEAREST` resampling. Returns a report string.
- `export_exact(filename, width, height=None)`: Exports at (nearest) exact target pixel size, warning if integer scaling can't match it.
