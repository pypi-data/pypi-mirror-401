import os
import shutil
import time
import zipfile

from typing import IO, BinaryIO

BUFFER_SIZE = 64 * 1024


def _copy_bytes(
    src: BinaryIO,
    dest: BinaryIO | IO[bytes],
    max_bytes: int,
    buffer_size: int = BUFFER_SIZE,
) -> None:
    """Copy up to max_bytes from src to dest in chunks."""
    remaining = max_bytes
    while remaining > 0:
        chunk = src.read(min(buffer_size, remaining))
        if not chunk:
            break
        dest.write(chunk)
        remaining -= len(chunk)


def zip_backup(src_folder: str, dest_zip: str, size_map: dict[str, int]) -> None:
    """
    Copies files directly into a ZIP archive, respecting a specific byte limit.
    """
    os.makedirs(os.path.dirname(dest_zip), exist_ok=True)

    folder_name = os.path.basename(src_folder.rstrip("/\\"))

    try:
        with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(src_folder):
                rel_root = os.path.relpath(root, src_folder)

                for filename in files:
                    src_path = os.path.join(root, filename)
                    rel_path = (
                        filename if rel_root == "." else f"{rel_root}/{filename}"
                    ).replace("\\", "/")
                    map_key = f"{folder_name}/{rel_path}"

                    file_size = os.path.getsize(src_path)
                    mod_time = os.path.getmtime(src_path)
                    date_time = time.localtime(mod_time)[:6]

                    zip_info = zipfile.ZipInfo(rel_path, date_time)
                    zip_info.compress_type = zipfile.ZIP_DEFLATED

                    with open(src_path, "rb") as f_src, zf.open(
                        zip_info, "w"
                    ) as f_dest:
                        limit = min(file_size, size_map.get(map_key, file_size))
                        _copy_bytes(f_src, f_dest, limit)
    except Exception as e:
        if os.path.exists(dest_zip):
            os.remove(dest_zip)
        raise e


def copy_backup(src_folder: str, dest_folder: str, size_map: dict[str, int]) -> None:
    """Copy files from source to destination, optionally truncating based on size mapping.

    Recursively copies all files from src_folder to dest_folder. Files listed in
    size_map will be truncated to the specified byte size if they exceed it.

    Args:
        src_folder: Path to the source folder to copy from.
        dest_folder: Path to the destination folder to copy to.
        size_map: Dictionary mapping file paths to maximum byte sizes.
            Files not in the mapping are copied in full.
            Example: {"world/level.dat": 1024}
    """
    os.makedirs(dest_folder, exist_ok=True)

    folder_name = os.path.basename(src_folder.rstrip("/\\"))

    try:
        for root, dirs, files in os.walk(src_folder):
            rel_root = os.path.relpath(root, src_folder)

            for filename in files:
                rel_path = (
                    filename if rel_root == "." else f"{rel_root}/{filename}"
                ).replace("\\", "/")

                src_path = os.path.join(root, filename)
                dest_path = os.path.join(dest_folder, rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                map_key = f"{folder_name}/{rel_path}"
                file_size = os.path.getsize(src_path)

                with open(src_path, "rb") as f_src, open(dest_path, "wb") as f_dest:
                    limit = min(file_size, size_map.get(map_key, file_size))
                    _copy_bytes(f_src, f_dest, limit)

                shutil.copystat(src_path, dest_path)
    except Exception as e:
        shutil.rmtree(dest_folder, True)
        raise e
