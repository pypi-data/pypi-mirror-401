from io import BytesIO
from pathlib import Path
from typing import Iterator

import pytz
from azure.core.credentials import TokenCredential
from azure.storage.blob import BlobPrefix, ContainerClient, StorageStreamDownloader

from azure_explorer.managers.container.base import ContainerManager
from azure_explorer.managers.models import FileProperties, FolderProperties

UTC = pytz.utc


class BlobStorageContainerManager(ContainerManager):
    def __init__(
        self,
        storage_account_name: str,
        container_name: str,
        credential: TokenCredential,
    ):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.credential = credential
        self.container_client = ContainerClient(
            f"https://{storage_account_name}.blob.core.windows.net",
            container_name=container_name,
            credential=credential,
        )

    def is_dir(self, path: Path | str) -> bool:
        if path == "":
            return True

        prefix = str(path).rstrip("/") + "/"

        try:
            first_blob = next(self.container_client.walk_blobs(name_starts_with=prefix))
        except StopIteration:
            return False

        if first_blob.name + "/" == prefix:
            return False

        return True

    def is_file(self, path: Path | str) -> bool:
        return self.container_client.get_blob_client(path).exists()

    def _iter_dir(self, path: Path | str, recursive: bool) -> Iterator[str]:
        if path == "":
            prefix = ""
        else:
            prefix = str(path).rstrip("/") + "/"

        for blob in self.container_client.walk_blobs(prefix, delimiter="/"):
            if not isinstance(blob, BlobPrefix):
                last_modified_time = blob.last_modified.replace(tzinfo=UTC)
                created_time = blob.creation_time.replace(tzinfo=UTC)
                yield FileProperties(
                    blob.name,
                    blob.size,
                    last_modified_time,
                    created_time,
                )
            else:
                if recursive:
                    yield from self._iter_dir(blob.name, recursive)
                else:
                    yield FolderProperties(
                        blob.name.rstrip("/"),
                        None,
                        None,
                        None,
                    )

    def _get_blob_stream_downloader(self, path: Path | str) -> StorageStreamDownloader:
        return self.container_client.download_blob(path)

    def _write_blob_data(
        self, path: Path | str, data: bytes | BytesIO, overwrite: bool = False
    ):
        self.container_client.upload_blob(path, data, overwrite=overwrite)

    def __repr__(self) -> str:
        return (
            "BlobStorageContainerManager("
            f"storage_account_name='{self.storage_account_name}', "
            f"container_name='{self.container_name}')"
        )
