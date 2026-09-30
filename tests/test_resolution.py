import os

from PIL import Image

from pixelspriteai import SpriteCanvas, MAX_LOGICAL_SIZE


def _tmp(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), name)


def test_free_non_square_resolution():
    canvas = SpriteCanvas(48, 16, scale_factor=8)
    assert (canvas.width, canvas.height) == (48, 16)
    assert canvas.image.size == (48, 16)
    assert canvas.info()["output_size"] == (384, 128)


def test_resolution_must_be_positive_integers():
    for bad in ((0, 16), (16, 0), (-4, 16)):
        try:
            SpriteCanvas(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{bad} should raise ValueError")

    for bad in ((16.5, 16), (16, "16"), (True, 16)):
        try:
            SpriteCanvas(*bad)
        except ValueError as exc:
            assert "integer" in str(exc)
        else:
            raise AssertionError(f"{bad} should raise ValueError")


def test_resolution_limit():
    try:
        SpriteCanvas(MAX_LOGICAL_SIZE + 1, 16)
    except ValueError as exc:
        assert "maximum logical size" in str(exc)
    else:
        raise AssertionError("oversized canvas should raise ValueError")


def test_set_resolution_keeps_pixels_topleft():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_pixel(1, 1, "red")
    res = canvas.set_resolution(32, 20)
    assert "Success" in res
    assert (canvas.width, canvas.height) == (32, 20)
    assert canvas.image.size == (32, 20)
    assert canvas.image.getpixel((1, 1)) == (255, 0, 0, 255)
    # new area is still transparent
    assert canvas.image.getpixel((31, 19)) == (0, 0, 0, 0)
    # drawing still works on the new grid
    assert canvas.draw_pixel(31, 19, "blue") == "Success"


def test_set_resolution_center_anchor_and_shrink():
    canvas = SpriteCanvas(16, 16)
    canvas.draw_pixel(8, 8, "red")  # dead center
    canvas.set_resolution(24, 24, anchor="center")
    # center of a 16x16 placed into 24x24 lands at (8+4, 8+4)
    assert canvas.image.getpixel((12, 12)) == (255, 0, 0, 255)

    canvas.set_resolution(4, 4, anchor="bottomleft")
    assert (canvas.width, canvas.height) == (4, 4)


def test_set_resolution_invalid_anchor():
    canvas = SpriteCanvas(16, 16)
    res = canvas.set_resolution(8, 8, anchor="middle")
    assert "Warning" in res
    assert (canvas.width, canvas.height) == (16, 16)


def test_set_scale_factor_and_warning():
    canvas = SpriteCanvas(16, 16)
    assert "Success" in canvas.set_scale_factor(3)
    assert canvas.scale_factor == 3

    res = canvas.set_scale_factor(0)
    assert "Warning" in res
    assert canvas.scale_factor == 3  # unchanged on failure


def test_export_override_and_report():
    canvas = SpriteCanvas(16, 16, scale_factor=1)
    canvas.draw_rectangle(0, 0, 7, 7, "red")

    filepath = _tmp("test_override.png")
    report = canvas.export(filepath, scale_factor=4)
    assert "Success" in report
    assert "64x64" in report
    assert canvas.scale_factor == 1  # the canvas default is untouched

    with Image.open(filepath) as img:
        assert img.size == (64, 64)
        assert img.getpixel((0, 0)) == (255, 0, 0, 255)
    os.remove(filepath)


def test_export_anisotropic_scale():
    canvas = SpriteCanvas(16, 16, scale_factor=(2, 3))
    filepath = _tmp("test_aniso.png")
    canvas.export(filepath)
    with Image.open(filepath) as img:
        assert img.size == (32, 48)
    os.remove(filepath)


def test_export_invalid_scale_warns_without_writing():
    canvas = SpriteCanvas(16, 16)
    filepath = _tmp("test_invalid.png")
    res = canvas.export(filepath, scale_factor=2.5)
    assert "Warning" in res
    assert not os.path.exists(filepath)


def test_export_exact_hit():
    canvas = SpriteCanvas(24, 24)
    filepath = _tmp("test_exact.png")
    report = canvas.export_exact(filepath, 96)
    assert "Warning" not in report
    with Image.open(filepath) as img:
        assert img.size == (96, 96)
    os.remove(filepath)


def test_export_exact_miss_warns_but_exports():
    canvas = SpriteCanvas(24, 24)
    filepath = _tmp("test_exact_miss.png")
    report = canvas.export_exact(filepath, 100)
    assert "Warning" in report
    with Image.open(filepath) as img:
        assert img.size == (96, 96)  # nearest integer factor
    os.remove(filepath)


def test_export_exact_invalid_target():
    canvas = SpriteCanvas(24, 24)
    res = canvas.export_exact(_tmp("test_exact_bad.png"), 0)
    assert "Warning" in res


def test_anisotropic_scale_survives_set_scale_factor():
    canvas = SpriteCanvas(16, 16)
    assert "Success" in canvas.set_scale_factor((2, 4))
    assert canvas.info()["output_size"] == (32, 64)
