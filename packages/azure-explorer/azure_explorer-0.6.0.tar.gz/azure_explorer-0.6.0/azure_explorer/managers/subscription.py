from azure.core.credentials import TokenCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.servicebus import ServiceBusManagementClient
from azure.mgmt.storage import StorageManagementClient

from azure_explorer.managers.base import Manager
from azure_explorer.managers.models import (
    ServiceBusProperties,
    StorageAccountProperties,
)
from azure_explorer.managers.service_bus import ServiceBusManager
from azure_explorer.managers.storage_account import StorageAccountManager


class SubscriptionManager(Manager):
    def __init__(self, subscription_id: str, credential: TokenCredential):
        self.subscription_id = subscription_id
        self.resource_mgtm_client = ResourceManagementClient(
            credential,
            subscription_id,
        )
        self.storage_mgtm_client = StorageManagementClient(
            credential,
            subscription_id,
        )
        self.servicebus_mgtm_client = ServiceBusManagementClient(
            credential,
            subscription_id,
        )
        self.credential = credential

    def list_storage_accounts(self) -> list[StorageAccountProperties]:
        items = []
        for storage_account in self.storage_mgtm_client.storage_accounts.list():
            item = StorageAccountProperties(
                storage_account.name,
                is_data_lake=storage_account.is_hns_enabled or False,
            )
            items.append(item)

        return items

    def list_storage_account_ids(self) -> list[str]:
        return [item.id for item in self.list_storage_accounts()]

    def list_storage_account_names(self) -> list[str]:
        return [item.name for item in self.list_storage_accounts()]

    def get_storage_account_manager(
        self, storage_account_name: str, is_data_lake: bool
    ):
        return StorageAccountManager(
            storage_account_name, self.credential, is_data_lake
        )

    def list_service_buses(self) -> list[ServiceBusProperties]:
        items = []
        for namespace in self.servicebus_mgtm_client.namespaces.list():
            item = ServiceBusProperties(
                namespace.name,
            )
            items.append(item)

        return items

    def list_service_bus_ids(self) -> list[str]:
        return [item.id for item in self.list_service_buses()]

    def list_service_bus_names(self) -> list[str]:
        return [item.name for item in self.list_service_buses()]

    def get_service_bus_manager(self, service_bus_name: str):
        return ServiceBusManager(service_bus_name, self.credential)

    def __repr__(self) -> str:
        return f"SubscriptionManager(subscription_id='{self.subscription_id}')"
