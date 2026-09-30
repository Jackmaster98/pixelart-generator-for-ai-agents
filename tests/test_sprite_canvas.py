import os
from PIL import Image
from pixelspriteai import SpriteCanvas

def test_initialization():
    canvas = SpriteCanvas(16, 16)
    assert canvas.width == 16
    assert canvas.height == 16
    assert canvas.scale_factor == 20
    assert canvas.image.size == (16, 16)
    assert canvas.image.mode == "RGBA"

    # check that it's completely transparent
    for x in range(16):
        for y in range(16):
            assert canvas.image.getpixel((x, y)) == (0, 0, 0, 0)

def test_draw_pixel():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_pixel(5, 5, "red")
    assert res == "Success"
    assert canvas.image.getpixel((5, 5)) == (255, 0, 0, 255)

def test_draw_pixel_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_pixel(16, 5, "red")
    assert "Warning" in res
    assert "out of bounds" in res

def test_draw_pixel_invalid_color():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_pixel(5, 5, "dark_magic")
    assert "Warning" in res
    assert "invalid" in res
    assert canvas.image.getpixel((5, 5)) == (255, 0, 255, 255) # fallback magenta

def test_draw_pixel_non_string_color():
    canvas = SpriteCanvas(16, 16)
    res = canvas.draw_pixel(5, 5, (255, 0, 0, 255))
    assert "Warning" in res
    assert canvas.image.getpixel((5, 5)) == (255, 0, 255, 255) # fallback magenta

def test_invalid_scale_factor():
    for bad in (0, -3):
        try:
            SpriteCanvas(16, 16, scale_factor=bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"scale_factor={bad} should raise ValueError")

    # Float scale factors are rejected: Image.resize only accepts integers,
    # so allowing 2.5 here would make export() crash later.
    try:
        SpriteCanvas(16, 16, scale_factor=2.5)
    except ValueError as exc:
        assert "integer" in str(exc)
    else:
        raise AssertionError("scale_factor=2.5 should raise ValueError")

def test_draw_line():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_line(1, 1, 3, 1, "blue")
    assert canvas.image.getpixel((1, 1)) == (0, 0, 255, 255)
    assert canvas.image.getpixel((2, 1)) == (0, 0, 255, 255)
    assert canvas.image.getpixel((3, 1)) == (0, 0, 255, 255)

def test_draw_rectangle_ordered():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_rectangle(2, 2, 4, 4, "#00FF00")
    for x in range(2, 5):
        for y in range(2, 5):
            assert canvas.image.getpixel((x, y)) == (0, 255, 0, 255)

def test_draw_rectangle_unordered():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_rectangle(4, 4, 2, 2, "#00FF00")
    for x in range(2, 5):
        for y in range(2, 5):
            assert canvas.image.getpixel((x, y)) == (0, 255, 0, 255)

def test_erase_pixel():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_pixel(5, 5, "red")
    canvas.erase_pixel(5, 5)
    assert canvas.image.getpixel((5, 5)) == (0, 0, 0, 0)

def test_erase_pixel_out_of_bounds():
    canvas = SpriteCanvas(16, 16)
    res = canvas.erase_pixel(18, 5)
    assert "Warning" in res
    assert "out of bounds" in res

def test_clear_canvas():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_rectangle(0, 0, 15, 15, "red")
    canvas.clear_canvas()
    for x in range(16):
        for y in range(16):
            assert canvas.image.getpixel((x, y)) == (0, 0, 0, 0)

def test_export():
    canvas = SpriteCanvas(16, 16, scale_factor=2)
    canvas.draw_rectangle(0, 0, 7, 7, "red")
    filename = "test_export.png"
    canvas.export(filename)

    assert os.path.exists(filename)

    with Image.open(filename) as exported_img:
        assert exported_img.size == (32, 32)
        assert exported_img.mode == "RGBA"

    os.remove(filename)
