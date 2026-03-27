from pathlib import Path
import pdf2image as p2i
import tempfile


def main():
    with tempfile.TemporaryDirectory() as tmp_dirname:
        data_dir = Path(__file__).parent.parent / "data"
        pages_dir = data_dir / "pages"
        pages_dir.mkdir(exist_ok=True, parents=True)
        work_dir = Path(tmp_dirname)
        work_dir.mkdir(exist_ok=True, parents=True)
        assert not list(work_dir.iterdir()), f"{work_dir} must be empty"
        pdf_path = (
            Path(__file__).parent.parent / "data" / "altniederlandische-malerei.pdf"
        )
        assert pdf_path.exists(), f"{pdf_path} must exist"
        print(pdf_path)
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
        print(f"Created {len(image_paths)} files in {pages_dir}")


if __name__ == "__main__":
    main()
