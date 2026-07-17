from PIL import Image, ImageDraw, ImageColor

class SpriteCanvas:
    def __init__(self, width: int, height: int, scale_factor: int = 20):
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    def _parse_color(self, color: str) -> tuple[tuple, str]:
        """Converts strings to RGBA tuple. Returns (color_tuple, warning_message)."""
        try:
            rgba = ImageColor.getcolor(color, "RGBA")
            return rgba, ""
        except ValueError:
            return (255, 0, 255, 255), f"Warning: Color '{color}' is invalid. Used fallback magenta (#FF00FF)."

    def _check_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def draw_pixel(self, x: int, y: int, color: str) -> str:
        if not self._check_bounds(x, y):
            return f"Warning: Coordinates ({x}, {y}) are out of bounds."

        parsed_color, warning = self._parse_color(color)
        self.image.putpixel((x, y), parsed_color)

        return warning if warning else "Success"

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: str) -> str:
        parsed_color, warning = self._parse_color(color)
        # Pillow handles drawing lines partially out of bounds gracefully,
        # but we can just pass them directly.
        self.draw.line((x1, y1, x2, y2), fill=parsed_color)

        return warning if warning else "Success"

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: str) -> str:
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)

        parsed_color, warning = self._parse_color(color)
        self.draw.rectangle((x_min, y_min, x_max, y_max), fill=parsed_color)

        return warning if warning else "Success"

    def erase_pixel(self, x: int, y: int) -> str:
        if not self._check_bounds(x, y):
            return f"Warning: Coordinates ({x}, {y}) are out of bounds."
        self.image.putpixel((x, y), (0, 0, 0, 0))
        return "Success"

    def clear_canvas(self) -> str:
        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        return "Success"

    def export(self, filename: str):
        # Resize using NEAREST to keep pixel art crisp
        new_width = self.width * self.scale_factor
        new_height = self.height * self.scale_factor
        resized_img = self.image.resize((new_width, new_height), resample=Image.NEAREST)
        resized_img.save(filename)
