from azure.core.credentials import TokenCredential
from azure.core.exceptions import HttpResponseError
from azure.data.tables import TableServiceClient
from azure.storage.blob import BlobServiceClient

from azure_explorer.managers import utils
from azure_explorer.managers.base import Manager
from azure_explorer.managers.container import (
    BlobStorageContainerManager,
    DataLakeContainerManager,
)


class StorageAccountManager(Manager):
    def __init__(
        self, storage_account_name: str, credential: TokenCredential, is_data_lake: bool
    ):
        self.storage_account_name = storage_account_name
        self.credential = credential
        self.blob_endpoint = f"{storage_account_name}.blob.core.windows.net"
        self.table_endpoint = f"{storage_account_name}.table.core.windows.net"
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{self.blob_endpoint}",
            credential=credential,
        )
        self.table_service_client = TableServiceClient(
            endpoint=f"https://{self.table_endpoint}",
            credential=credential,
        )
        self.is_data_lake = is_data_lake

    def check_access(self, data_object_type: str) -> bool:
        if data_object_type == "container":
            utils.check_connection(self.blob_endpoint)
            try:
                next(self.blob_service_client.list_containers())
            except HttpResponseError as exc:
                raise exc
            except Exception as exc:
                raise exc
        elif data_object_type == "table":
            next(self.table_service_client.list_tables())
        else:
            raise ValueError(f"Unknown data object type: {data_object_type}")
        return True

    def get_container_manager(
        self, container_name: str
    ) -> DataLakeContainerManager | BlobStorageContainerManager:
        if self.is_data_lake:
            return DataLakeContainerManager(
                self.storage_account_name,
                container_name,
                self.credential,
            )
        else:
            return BlobStorageContainerManager(
                self.storage_account_name,
                container_name,
                self.credential,
            )

    def list_container_names(self) -> list[str]:
        return [
            container.name for container in self.blob_service_client.list_containers()
        ]

    def list_table_names(self) -> list[str]:
        return [table.name for table in self.table_service_client.list_tables()]

    def __repr__(self) -> str:
        return (
            "StorageAccountManager("
            f"storage_account_name='{self.storage_account_name}', "
            f"is_data_lake={self.is_data_lake})"
        )
