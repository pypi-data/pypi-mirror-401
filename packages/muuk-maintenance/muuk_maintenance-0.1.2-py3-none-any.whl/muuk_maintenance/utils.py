import os
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, Tuple
from urllib.parse import urlparse

import requests


def ensure_dir(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    if not path.is_dir():
        raise ValueError(f"{label} must be a directory: {path}")


def _zip_dirs_to_temp(paths: Iterable[Path]) -> Tuple[str, str]:
    fd, zip_path = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root in paths:
            base = root.resolve()
            for p in base.rglob("*"):
                if p.is_file():
                    arcname = str(p.relative_to(base))
                    zf.write(p, arcname=f"{base.name}/{arcname}")
    return zip_path, os.path.basename(zip_path)


def create_temp_zip(test_files_dir: Path, failure_data_dir: Path) -> str:
    zip_path, _ = _zip_dirs_to_temp([test_files_dir, failure_data_dir])
    return zip_path


def request_signed_url(muuk_key: str, endpoint: str) -> Tuple[str, str]:
    r = requests.post(
        endpoint,
        json={"key": muuk_key},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if "sourcePath" not in data or "signedUrl" not in data:
        raise ValueError("Signed URL response missing sourcePath or signedUrl")
    return data["sourcePath"], data["signedUrl"]


def upload_zip_to_s3(zip_path: str, signed_url: str) -> None:
    with open(zip_path, "rb") as f:
        r = requests.put(
            signed_url,
            data=f,
            headers={
                "Content-Type": "application/zip",
                "x-amz-meta-purpose": "muukmcp",
                "x-amz-server-side-encryption": "AES256",
            },
            timeout=300,
        )
    r.raise_for_status()


def build_s3_path(source_path: str, signed_url: str) -> str:
    """Build a full HTTPS path for the uploaded zip directory."""
    parsed = urlparse(signed_url)
    if not parsed.scheme or not parsed.netloc:
        return source_path

    base = f"{parsed.scheme}://{parsed.netloc}"
    signed_path = parsed.path
    normalized_source = source_path.strip("/")

    if normalized_source and normalized_source in signed_path:
        prefix, _ = signed_path.split(normalized_source, 1)
        return f"{base}{prefix}{normalized_source}/"

    if "/" in signed_path:
        dir_path = signed_path.rsplit("/", 1)[0]
        return f"{base}{dir_path}/"

    return f"{base}/"
