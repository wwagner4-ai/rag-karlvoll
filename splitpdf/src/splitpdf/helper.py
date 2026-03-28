from pathlib import Path
import shutil

COLLECTION_NAME = "pages"


def clear_dir(target_dir: Path) -> None:
    for item in target_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def is_empty_dir(target_dir: Path) -> bool:
    return bool(list(target_dir.iterdir()))


def data_dir() -> Path:
    return Path(__file__).parent.parent.parent.parent / "data"


def pages_dir() -> Path:
    return data_dir() / "pages"


def texts_dir() -> Path:
    return data_dir() / "texts"
