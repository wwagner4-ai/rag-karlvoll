import splitpdf.helper as hlp_
import splitpdf.embed as em_
import tempfile
from pathlib import Path


def run():
    print("--> tryout")

    with em_.VectorDatabase() as db:
        docs = db.query(hlp_.COLLECTION_NAME, "Hallo wie gehts")
        print(f"### found {len(docs)} docs in the embeddings")
        for i, doc in enumerate(docs):
            print(f"{i:10d} {doc}")
            print("-" * 100)

    print("<-- tryout")


def tryout_minio():
    data_dir = hlp_.data_dir()
    txt_dir = data_dir / "text"
    txt_dir.mkdir(exist_ok=True, parents=True)
    with tempfile.TemporaryDirectory() as tmp_dirname:
        tmp_dir = Path(tmp_dirname)
        print(f"### {tmp_dir} {tmp_dir.exists()}")
        file = tmp_dir / "t2.txt"
        file.write_text("Ich bin ein test")
        hlp_.copy_file(file, txt_dir / "out002.txt")
