from azure_explorer.config import Config
from azure_explorer.managers import (
    ContainerManager,
    ServiceBusManager,
    StorageAccountManager,
    SubscriptionManager,
    TenantManager,
)


def get_tenant_manager() -> TenantManager:
    return TenantManager(
        credential=Config.credential,
    )


def get_subscription_manager(subscription_id: str) -> SubscriptionManager:
    return SubscriptionManager(
        subscription_id=subscription_id,
        credential=Config.credential,
    )


def get_storage_account_manager(
    storage_account_name: str,
) -> StorageAccountManager:
    return StorageAccountManager(storage_account_name, credential=Config.credential)


def get_container_manager(
    storage_account_name: str,
    container_name: str,
    is_data_lake: bool = False,
) -> ContainerManager:
    return ContainerManager.create(
        storage_account_name, container_name, is_data_lake, credential=Config.credential
    )


def get_service_bus_manager(
    service_bus_name: str,
) -> ServiceBusManager:
    return ServiceBusManager(
        service_bus_name=service_bus_name,
        credential=Config.credential,
    )


def read_file(
    storage_account_name: str,
    container_name: str,
    path: str,
) -> bytes:
    container_manager = get_container_manager(
        storage_account_name, container_name, is_data_lake=False
    )
    return container_manager.read_file(path)
