import splitpdf.helper as hlp_
import tempfile
from pathlib import Path


def run():

    print("--> tryout")
    data_dir = hlp_.data_dir()
    txt_dir = data_dir / "text"
    txt_dir.mkdir(exist_ok=True, parents=True)
    with tempfile.TemporaryDirectory() as tmp_dirname:
        tmp_dir = Path(tmp_dirname)
        print(f"### {tmp_dir} {tmp_dir.exists()}")
        file = tmp_dir / "t2.txt"
        file.write_text("Ich bin ein test")
        hlp_.copy_file(file, txt_dir / "out002.txt")
    print("<-- tryout")
