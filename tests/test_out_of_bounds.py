from pixelspriteai import SpriteCanvas

def test_line_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_line(-5, -5, 20, 20, "red")
    assert "Warning" in res
    assert "out of bounds" in res
    # Pillow clips the line to the canvas: the main diagonal is drawn.
    for i in range(16):
        assert canvas.image.getpixel((i, i)) == (255, 0, 0, 255)

def test_rectangle_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_rectangle(-5, -5, 20, 20, "red")
    assert "Warning" in res
    assert "out of bounds" in res
    # The rectangle is clamped to the canvas, filling it entirely.
    for x in range(16):
        for y in range(16):
            assert canvas.image.getpixel((x, y)) == (255, 0, 0, 255)
