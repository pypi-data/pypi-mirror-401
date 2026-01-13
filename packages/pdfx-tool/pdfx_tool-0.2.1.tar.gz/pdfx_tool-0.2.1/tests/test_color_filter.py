import tempfile
from pathlib import Path
from pdfx import main


def test_parse_color_string():
    # Test hex format
    assert main.parse_color_string("#FF0000") == (255, 0, 0)

    # Test RGB format
    assert main.parse_color_string("255,0,128") == (255, 0, 128)

    # Test named colors
    assert main.parse_color_string("red") == (255, 0, 0)
    assert main.parse_color_string("blue") == (0, 0, 255)
    assert main.parse_color_string("green") == (0, 128, 0)
    assert main.parse_color_string("white") == (255, 255, 255)
    assert main.parse_color_string("black") == (0, 0, 0)

    # Test case insensitivity for named colors
    assert main.parse_color_string("RED") == (255, 0, 0)
    assert main.parse_color_string("Blue") == (0, 0, 255)


# Basic smoke test that runs the filter function on a tiny programmatic PDF
def test_filter_pdf_by_color_smoke():
    try:
        import fitz
    except Exception:
        # If PyMuPDF isn't installed, just skip this functional test
        return

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "red text", fontsize=12,
                     fontname="helv", color=(1, 0, 0))
    page.insert_text((50, 80), "blue text", fontsize=12,
                     fontname="helv", color=(0, 0, 1))

    with tempfile.TemporaryDirectory() as d:
        in_path = Path(d) / "test.pdf"
        out_path = Path(d) / "out.pdf"
        doc.save(str(in_path))
        doc.close()

        written = main.filter_pdf_by_color(
            in_path, out_path, (255, 0, 0), tolerance=5.0)
        assert written == 1
        assert out_path.exists()
