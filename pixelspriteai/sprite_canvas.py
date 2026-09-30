from PIL import Image, ImageDraw, ImageColor

# --- Limits -----------------------------------------------------------------
# They are not creative limits: they exist to protect RAM (and the agent's own
# token budget) from absurd requests like "make me a 50000x50000 sprite".
MAX_LOGICAL_SIZE = 1024   # max width/height of the *pixel grid*
MAX_OUTPUT_SIZE = 8192    # max width/height of the exported PNG, in real pixels


class SpriteCanvas:
    """
    A transparent pixel-art canvas driven by geometric primitives.

    The *logical* size (the pixel grid you draw on) and the *export* size (how
    big the PNG comes out) are two independent decisions. The agent is free to
    choose both, and to change its mind later via `set_resolution`,
    `set_scale_factor` or the per-call override on `export`.
    """

    def __init__(self, width: int, height: int, scale_factor: int = 20):
        self.width, self.height = self._validate_resolution(width, height)
        # Keeps the public attribute identical to what was passed (tests and
        # existing scripts rely on `canvas.scale_factor` being an int).
        self.scale_factor = scale_factor
        self._validate_scale_factor(scale_factor)  # early and explicit failure

        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)

    # --- Validation helpers -------------------------------------------------
    @staticmethod
    def _validate_resolution(width, height):
        """Any positive integer pair up to MAX_LOGICAL_SIZE. Non-square is fine."""
        for name, value in (("width", width), ("height", height)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(
                    f"{name} must be an integer number of pixels, got {value!r}."
                )
            if value < 1:
                raise ValueError(f"{name} must be at least 1 pixel, got {value}.")

        too_big = [
            f"{name}={value}"
            for name, value in (("width", width), ("height", height))
            if value > MAX_LOGICAL_SIZE
        ]
        if too_big:
            raise ValueError(
                f"{', '.join(too_big)} exceeds the maximum logical size of "
                f"{MAX_LOGICAL_SIZE}px. Pick a smaller grid: you only need detail "
                f"in the drawing, the export can enlarge it afterwards."
            )
        return width, height

    @staticmethod
    def _validate_scale_factor(scale_factor):
        """Accepts a positive int or a (x, y) int tuple. Returns the (sx, sy) pair."""
        if isinstance(scale_factor, (tuple, list)) and len(scale_factor) == 2:
            sx, sy = scale_factor
        else:
            sx = sy = scale_factor

        for name, value in (("scale_factor", sx), ("scale_factor", sy)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(
                    f"{name} must be an integer greater than or equal to 1, "
                    f"got {value!r}. Image resizing does not accept fractional scales."
                )
            if value < 1:
                raise ValueError(f"{name} must be an integer greater than or equal to 1.")
        return sx, sy

    # --- Resolution control -------------------------------------------------
    def set_resolution(self, width: int, height: int, anchor: str = "topleft") -> str:
        """
        Change the logical canvas size on the fly, *keeping what is already
        drawn*. Much cheaper than starting over when you realise you need room.

        anchor: "topleft" (default), "center" or "bottomleft".
        """
        new_w, new_h = self._validate_resolution(width, height)
        anchors = ("topleft", "center", "bottomleft")
        if anchor not in anchors:
            return f"Warning: anchor '{anchor}' is invalid. Use one of {anchors}. Canvas unchanged."

        if anchor == "topleft":
            dx, dy = 0, 0
        elif anchor == "center":
            dx, dy = (new_w - self.width) // 2, (new_h - self.height) // 2
        else:  # bottomleft
            dx, dy = 0, new_h - self.height

        new_img = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))

        # Paste the old content, clipping it if the new canvas is smaller.
        sx0, sy0 = max(0, -dx), max(0, -dy)
        dx0, dy0 = max(0, dx), max(0, dy)
        crop_w = min(self.width - sx0, new_w - dx0)
        crop_h = min(self.height - sy0, new_h - dy0)
        if crop_w > 0 and crop_h > 0:
            new_img.paste(
                self.image.crop((sx0, sy0, sx0 + crop_w, sy0 + crop_h)), (dx0, dy0)
            )

        self.width, self.height = new_w, new_h
        self.image = new_img
        self.draw = ImageDraw.Draw(self.image)
        return f"Success: canvas resized to {new_w}x{new_h} (anchor: {anchor})."

    def set_scale_factor(self, scale_factor) -> str:
        """Change the export magnification used by default by `export()`."""
        try:
            sx, sy = self._validate_scale_factor(scale_factor)
        except ValueError as exc:
            return f"Warning: {exc} Canvas and export settings unchanged."
        self.scale_factor = scale_factor
        return f"Success: scale factor set to {sx if sx == sy else (sx, sy)}."

    def info(self) -> dict:
        """Everything worth knowing about the current resolution."""
        sx, sy = self._validate_scale_factor(self.scale_factor)
        return {
            "width": self.width,
            "height": self.height,
            "scale_factor": self.scale_factor,
            "output_size": (self.width * sx, self.height * sy),
            "pixel_count": self.width * self.height,
            "max_logical_size": MAX_LOGICAL_SIZE,
            "max_output_size": MAX_OUTPUT_SIZE,
        }

    # --- Colors and drawing -------------------------------------------------
    def _parse_color(self, color: str) -> tuple:
        """Converts strings to RGBA tuple. Returns (color_tuple, warning_message)."""
        try:
            rgba = ImageColor.getcolor(color, "RGBA")
            return rgba, ""
        except (ValueError, TypeError, AttributeError):
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
        # clipping them to the canvas.
        self.draw.line((x1, y1, x2, y2), fill=parsed_color)

        if not (self._check_bounds(x1, y1) and self._check_bounds(x2, y2)):
            bounds_warning = f"Warning: Coordinates ({x1}, {y1}) to ({x2}, {y2}) are out of bounds."
            return f"{bounds_warning} {warning}" if warning else bounds_warning

        return warning if warning else "Success"

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: str) -> str:
        x_min, x_max = min(x1, x2), max(x1, x2)
        y_min, y_max = min(y1, y2), max(y1, y2)

        parsed_color, warning = self._parse_color(color)
        self.draw.rectangle((x_min, y_min, x_max, y_max), fill=parsed_color)

        if not (self._check_bounds(x1, y1) and self._check_bounds(x2, y2)):
            bounds_warning = f"Warning: Coordinates ({x1}, {y1}) to ({x2}, {y2}) are out of bounds."
            return f"{bounds_warning} {warning}" if warning else bounds_warning

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

    # --- Export -------------------------------------------------------------
    def export(self, filename: str, scale_factor=None) -> str:
        """
        Save the canvas as a PNG, scaled with NEAREST resampling (crisp edges).

        scale_factor: overrides the canvas default for this export only.
                      Accepts an int (uniform) or a (x, y) tuple (anisotropic).
        """
        try:
            sx, sy = self._validate_scale_factor(
                self.scale_factor if scale_factor is None else scale_factor
            )
        except ValueError as exc:
            return f"Warning: {exc} Nothing was exported."

        new_width, new_height = self.width * sx, self.height * sy
        resized_img = self.image.resize((new_width, new_height), resample=Image.NEAREST)
        resized_img.save(filename)

        factor_str = f"{sx}x" if sx == sy else f"{sx}x horizontally, {sy}x vertically"
        report = (
            f"Success: exported '{filename}' ({self.width}x{self.height} grid at "
            f"{factor_str} -> {new_width}x{new_height} px)."
        )
        if new_width > MAX_OUTPUT_SIZE or new_height > MAX_OUTPUT_SIZE:
            report = (
                f"Warning: output {new_width}x{new_height} px exceeds the recommended "
                f"maximum of {MAX_OUTPUT_SIZE}px; consider a smaller scale factor. " + report
            )
        return report

    def export_exact(self, filename: str, width: int, height: int = None) -> str:
        """
        Export to an *exact* target pixel size (e.g. 96x96 for an atlas slot).

        Uses the nearest integer scale factor and warns when the target is not
        an exact multiple of the grid (that would require interpolation, and it
        would blur the pixel art).
        """
        height = width if height is None else height
        for name, value in (("width", width), ("height", height)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                return f"Warning: target {name} must be a positive integer, got {value!r}. Nothing was exported."

        sx = max(1, round(width / self.width))
        sy = max(1, round(height / self.height))
        report = self.export(filename, scale_factor=(sx, sy))

        warnings = []
        if self.width * sx != width or self.height * sy != height:
            warnings.append(
                f"Warning: {self.width}x{self.height} cannot reach exactly {width}x{height} "
                f"with integer scaling; exported {self.width * sx}x{self.height * sy} instead "
                f"(a divisible grid is required for sharp pixels)."
            )
        return " ".join(warnings + [report]) if warnings else report
