import os
from pathlib import Path


class StorageRepository:
    STORAGE_PATH = Path("files")

    def __init__(self):
        if not os.path.exists(self.STORAGE_PATH):
            os.mkdir(self.STORAGE_PATH)

    def store(self, filename: str, body: bytes):
        with open(self.STORAGE_PATH / filename, "wb") as f:
            f.write(body)

    def get(self, filename: str) -> bytes | None:
        if not os.path.exists(self.STORAGE_PATH / filename):
            return None
        with open(self.STORAGE_PATH / filename, "rb") as f:
            return f.read()
