import os
from pathlib import Path

from vercel import blob


DATA_DIR = Path("data")
DATASET_EXTENSIONS = (".csv", ".xlsx")


def _uses_blob_storage() -> bool:
    return os.getenv("VERCEL") == "1"


async def save_dataset(dataset_id: str, extension: str, contents: bytes) -> None:
    if _uses_blob_storage():
        await blob.put_blob(
            f"datasets/{dataset_id}{extension}",
            contents,
            access="private",
            content_type=(
                "text/csv" if extension == ".csv" else
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ),
        )
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / f"{dataset_id}{extension}").write_bytes(contents)


async def load_dataset(dataset_id: str) -> tuple[str, bytes] | None:
    if _uses_blob_storage():
        for extension in DATASET_EXTENSIONS:
            try:
                result = await blob.get_blob(
                    f"datasets/{dataset_id}{extension}",
                    access="private",
                )
                return extension, result.body
            except blob.BlobNotFoundError:
                continue
        return None

    for extension in DATASET_EXTENSIONS:
        path = DATA_DIR / f"{dataset_id}{extension}"
        if path.is_file():
            return extension, path.read_bytes()
    return None