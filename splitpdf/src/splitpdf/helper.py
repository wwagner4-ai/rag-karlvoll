from pathlib import Path
import shutil


def clear_dir(target_dir: Path) -> None:
    for item in target_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def is_empty_dir(target_dir: Path) -> bool:
    return bool(list(target_dir.iterdir()))
