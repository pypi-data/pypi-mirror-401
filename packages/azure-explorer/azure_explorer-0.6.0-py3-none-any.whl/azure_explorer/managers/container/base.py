from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path
from typing import Iterator

from azure.core.credentials import TokenCredential
from azure.storage.blob import StorageStreamDownloader

from azure_explorer.managers.models import FileProperties, FolderProperties


class FolderNotFoundError(Exception):
    pass


class FileOrFolderNotFoundError(Exception):
    pass


class ContainerManager(ABC):
    @staticmethod
    def create(
        storage_account_name: str,
        container_name: str,
        is_data_lake: bool,
        credential: TokenCredential,
    ):
        from . import BlobStorageContainerManager, DataLakeContainerManager

        if is_data_lake:
            return DataLakeContainerManager(
                storage_account_name=storage_account_name,
                container_name=container_name,
                credential=credential,
            )
        else:
            return BlobStorageContainerManager(
                storage_account_name=storage_account_name,
                container_name=container_name,
                credential=credential,
            )

    @abstractmethod
    def _get_blob_stream_downloader(self, path: Path | str) -> StorageStreamDownloader:
        ...

    @abstractmethod
    def _write_blob_data(
        self, path: Path | str, data: bytes | BytesIO, overwrite: bool = False
    ):
        ...

    @abstractmethod
    def _iter_dir(
        self,
        path: Path | str,
        recursive: bool,
    ) -> Iterator[FileProperties | FolderProperties]:
        ...

    @abstractmethod
    def is_dir(self, path: Path | str) -> bool:
        ...

    @abstractmethod
    def is_file(self, path: Path | str) -> bool:
        ...

    def iter_dir(
        self, path: Path | str = "", recursive: bool = False
    ) -> Iterator[FileProperties | FolderProperties]:
        if not self.is_dir(path):
            raise FolderNotFoundError(path)

        yield from self._iter_dir(path, recursive)

    def list_dir(
        self, path: Path | str = "", recursive: bool = False
    ) -> list[FileProperties | FolderProperties]:
        return list(self.iter_dir(path, recursive))

    def read_file(self, path: Path | str) -> bytes:
        if not self.is_file(path):
            raise FileNotFoundError(path)

        blob_stream_downloader = self._get_blob_stream_downloader(path)

        return blob_stream_downloader.readall()

    def download_file(self, source: Path | str, destination: Path | str):
        destination = Path(destination)

        if not self.is_file(source):
            raise FileNotFoundError(source)

        destination.parent.mkdir(parents=True, exist_ok=True)

        blob_stream_downloader = self._get_blob_stream_downloader(source)

        with open(destination, "wb") as f:
            blob_stream_downloader.readinto(f)

    def download_dir(self, source: Path | str, destination: Path):
        destination = Path(destination)

        for subsource in self.iter_dir(source, recursive=True):
            subdestination = destination / Path(subsource.path)
            self.download_file(subsource.path, subdestination)

    def write_blob(self, data: bytes, path: Path | str, overwrite: bool = False):
        self._write_blob_data(path, data, overwrite=overwrite)

    def upload_file(self, source: Path | str, path: str, overwrite: bool = False):
        with open(source, "rb") as f:
            self._write_blob_data(path, f, overwrite=overwrite)

    def upload_dir(
        self, source: Path | str, destination: Path | str, overwrite: bool = False
    ):
        # NOTE: Will not create empty folders
        destination = Path(destination)
        source = Path(source)

        for subsource in source.rglob("*"):
            if not subsource.is_file():
                continue

            subdestination = str(destination / subsource.relative_to(source))

            self.upload_file(subsource, subdestination, overwrite)
