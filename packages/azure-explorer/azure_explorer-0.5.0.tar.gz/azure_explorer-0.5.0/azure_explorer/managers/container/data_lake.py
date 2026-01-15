from io import BytesIO
from pathlib import Path
from typing import Iterator

import pytz
from azure.core.credentials import TokenCredential
from azure.storage.filedatalake import FileSystemClient, StorageStreamDownloader

from azure_explorer.managers.container.base import ContainerManager
from azure_explorer.managers.models import FileProperties, FolderProperties

UTC = pytz.utc


class DataLakeContainerManager(ContainerManager):
    def __init__(
        self,
        storage_account_name: str,
        container_name: str,
        credential: TokenCredential,
    ):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.credential = credential
        self.file_system_client = FileSystemClient(
            f"https://{storage_account_name}.dfs.core.windows.net",
            file_system_name=container_name,
            credential=credential,
        )

    def is_dir(self, folder: Path | str) -> bool:
        # checking if a folder exist is a bit tricky, but
        # we use the solution proposed here in
        # https://github.com/Azure/azure-sdk-for-python/issues/24814
        if folder == "":
            return True

        file_client = self.file_system_client.get_file_client(folder)
        if not file_client.exists():
            return False

        file_metadata = file_client.get_file_properties().metadata
        is_dir_blob = file_metadata.get("hdi_isfolder", "false").lower() == "true"
        if not is_dir_blob:
            return False

        return True

    def is_file(self, path: Path | str):
        if path == "":
            return False

        file_client = self.file_system_client.get_file_client(path)
        if not file_client.exists():
            return False

        file_metadata = file_client.get_file_properties().metadata
        is_dir_blob = file_metadata.get("hdi_isfolder", "false").lower() == "true"
        if is_dir_blob:
            return False

        return True

    def _iter_dir(
        self,
        folder: Path | str,
        recursive: bool,
    ) -> Iterator[FileProperties | FolderProperties]:
        for path in self.file_system_client.get_paths(folder, recursive):
            last_modified_time = path.last_modified.replace(tzinfo=UTC)
            created_time = path.creation_time.replace(tzinfo=UTC)

            if path.is_directory:
                if recursive:
                    continue
                yield FolderProperties(
                    path.name, None, last_modified_time, created_time
                )
            else:
                yield FileProperties(
                    path.name, path.content_length, last_modified_time, created_time
                )

    def _get_blob_stream_downloader(self, path: Path | str) -> StorageStreamDownloader:
        file_client = self.file_system_client.get_file_client(path)
        return file_client.download_file()

    def _write_blob_data(
        self, path: Path | str, data: bytes | BytesIO, overwrite: bool = False
    ):
        file_client = self.file_system_client.get_file_client(path)
        file_client.upload_data(data, overwrite=overwrite)

    def __repr__(self) -> str:
        return (
            "DataLakeContainerManager("
            f"storage_account_name='{self.storage_account_name}', "
            f"container_name='{self.container_name}')"
        )
