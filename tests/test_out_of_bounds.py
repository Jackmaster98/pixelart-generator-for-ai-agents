from pixelspriteai import SpriteCanvas

def test_line_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_line(-5, -5, 20, 20, "red")
    # Should not crash

def test_rectangle_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_rectangle(-5, -5, 20, 20, "red")
    # Should not crash
