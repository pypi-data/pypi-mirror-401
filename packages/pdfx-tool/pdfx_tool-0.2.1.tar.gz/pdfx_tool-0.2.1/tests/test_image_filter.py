import tempfile
from pathlib import Path
from pdfx import main


def test_apply_image_filter_smoke():
    try:
        import fitz
        from PIL import Image
    except Exception:
        # skip if dependencies aren't available
        return

    # create a tiny 1-page PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello", fontsize=40, fontname="helv", color=(1, 0, 0))

    with tempfile.TemporaryDirectory() as d:
        in_path = Path(d) / "imgtest.pdf"
        out_path = Path(d) / "imgtest_out.pdf"
        doc.save(str(in_path))
        doc.close()

        written = main.apply_image_filter_to_pdf(in_path, out_path, filter_name="bw", strength=128)
        assert written == 1
        assert out_path.exists()
