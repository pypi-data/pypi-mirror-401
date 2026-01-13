import tempfile
from pathlib import Path
from pdfx import main


def test_recolor_smoke():
    try:
        import fitz
    except Exception:
        return
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "red text", fontsize=20,
                     fontname="helv", color=(1, 0, 0))
    with tempfile.TemporaryDirectory() as d:
        in_path = Path(d) / "rc.pdf"
        out_path = Path(d) / "rc_out.pdf"
        doc.save(str(in_path))
        doc.close()
        pages = main.recolor_pdf_text(
            in_path, out_path, (255, 0, 0), (0, 0, 255), tolerance=10.0)
        assert pages == 1
        assert out_path.exists()


def test_ocr_smoke():
    try:
        import fitz
        import pytesseract
    except Exception:
        return
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello OCR", fontsize=20,
                     fontname="helv", color=(0, 0, 0))
    with tempfile.TemporaryDirectory() as d:
        in_path = Path(d) / "ocr.pdf"
        out_path = Path(d) / "ocr_out.pdf"
        doc.save(str(in_path))
        doc.close()
        pages = main.ocr_make_searchable(in_path, out_path, lang="eng")
        assert pages == 1
        assert out_path.exists()
