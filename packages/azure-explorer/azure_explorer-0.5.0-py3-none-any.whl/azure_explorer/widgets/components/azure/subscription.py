from typing import Iterator

from textual.widget import Widget

from azure_explorer.managers import SubscriptionManager
from azure_explorer.widgets.components.azure.service_bus import EntitySelector
from azure_explorer.widgets.components.azure.storage_account import (
    DataObjectTypeSelector,
)
from azure_explorer.widgets.components.windows import Browser, Selector


class ResourceTypeSelector(Selector):
    def __init__(self, sub_manager: SubscriptionManager):
        self.sub_manager = sub_manager
        super().__init__()

    def iter_options(self):
        yield ("storage_account", "Storage Accounts")
        yield ("data_lake", "Data Lakes")
        yield ("service_bus", "Service Buses")

    def get_option_widget(self, id_):
        if id_ == "storage_account":
            return StorageAccountBrowser(self.sub_manager, is_data_lake=False)
        elif id_ == "data_lake":
            return StorageAccountBrowser(self.sub_manager, is_data_lake=True)
        elif id_ == "service_bus":
            return ServiceBusBrowser(self.sub_manager)


class StorageAccountBrowser(Browser):
    COLUMN_NAMES = ["Name"]

    def __init__(self, subscription_manager: SubscriptionManager, is_data_lake: bool):
        self.subscription_manager = subscription_manager
        self.is_data_lake = is_data_lake
        super().__init__()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for storage_account in self.subscription_manager.list_storage_accounts():
            if storage_account.is_data_lake == self.is_data_lake:
                yield storage_account.name, (storage_account.name,)

    def get_item_widget(self, id_: str) -> Widget:
        sa_manager = self.subscription_manager.get_storage_account_manager(
            storage_account_name=id_,
            is_data_lake=self.is_data_lake,
        )

        return DataObjectTypeSelector(sa_manager)


class ServiceBusBrowser(Browser):
    COLUMN_NAMES = ["Name"]

    def __init__(self, subscription_manager: SubscriptionManager):
        self.subscription_manager = subscription_manager
        super().__init__()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for sb in self.subscription_manager.list_service_buses():
            yield sb.name, (sb.name,)

    def get_item_widget(self, item: str) -> Widget:
        sb_manager = self.subscription_manager.get_service_bus_manager(
            service_bus_name=item,
        )
        return EntitySelector(sb_manager)
