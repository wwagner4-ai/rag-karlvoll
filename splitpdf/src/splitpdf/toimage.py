from pathlib import Path
import pdf2image as p2i
import tempfile
import splitpdf.helper as hlp_


def toimage(clear_out_dir: bool):
    with tempfile.TemporaryDirectory() as tmp_dirname:
        pages_dir = hlp_.pages_dir()
        pages_dir.mkdir(exist_ok=True, parents=True)
        if clear_out_dir:
            hlp_.clear_dir(pages_dir)
        assert not hlp_.is_empty_dir(pages_dir), f"{pages_dir} must be empty"
        work_dir = Path(tmp_dirname)
        work_dir.mkdir(exist_ok=True, parents=True)
        assert not list(work_dir.iterdir()), f"{work_dir} must be empty"
        pdf_path = hlp_.data_dir() / "altniederlandische-malerei.pdf"
        assert pdf_path.exists(), f"{pdf_path} must exist"
        print(f"Reading pdf file: {pdf_path}")
        pdf_bytes: bytes = pdf_path.read_bytes()
        image_paths = p2i.convert_from_bytes(
            pdf_bytes,
            first_page=10,
            last_page=337,
            paths_only=True,
            jpegopt={"quality": "70", "progressive": True, "optimize": True},
            fmt="jpeg",
            output_folder=work_dir,
        )
        for i, image in enumerate(work_dir.iterdir()):
            image.rename(pages_dir / f"page-{i:04d}.jpg")
        print(f"Created {len(image_paths)} files from {pdf_path} in {pages_dir}")
