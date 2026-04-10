import os
from pathlib import Path
from enum import Enum
import boto3
from s3path import S3Path, register_configuration_parameter
from botocore.client import Config


COLLECTION_NAME = "pages"


def clear_dir(pth: Path, depth: int = 0) -> None:
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            clear_dir(child, depth + 1)
    if depth > 0 and pth.exists():
        pth.rmdir()


def is_empty_dir(target_dir: Path) -> bool:
    return not bool(list(target_dir.iterdir()))


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if name is None:
        raise ValueError(f"Environment variable '{name}' not defined")
    return value


def data_dir() -> Path:
    # return Path(__file__).parent.parent.parent.parent / "data"
    url = get_env("MINIO_URL")
    user = get_env("MINIO_USER")
    password = get_env("MINIO_PASSWORD")
    return bucket_as_path("data", url, user, password)


def pages_dir() -> Path:
    return data_dir() / "pages"


def texts_dir() -> Path:
    return data_dir() / "texts"


def copy_file(file: Path, dest: Path):
    dest.write_bytes(file.read_bytes())


class AddressingStyle(Enum):
    PATH = "path"
    VIRTUAL = "virtual"
    AUTO = "auto"


def bucket_as_path(
    bucket_name: str,
    url: str,
    user: str,
    password: str,
    addressing_style: AddressingStyle = AddressingStyle.AUTO,
) -> Path:
    minio_config = Config(s3={"addressing_style": addressing_style.value})
    resource = boto3.resource(
        "s3",
        endpoint_url=url,
        aws_access_key_id=user,
        aws_secret_access_key=password,
        config=minio_config,
    )
    register_configuration_parameter(S3Path("/"), resource=resource)
    return S3Path(f"/{bucket_name}")
