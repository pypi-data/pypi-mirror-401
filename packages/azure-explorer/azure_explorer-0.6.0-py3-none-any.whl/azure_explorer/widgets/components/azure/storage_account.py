from typing import Iterator

from textual.widget import Widget

from azure_explorer.managers import StorageAccountManager
from azure_explorer.widgets.components.azure.container import BlobFolderBrowser
from azure_explorer.widgets.components.windows import Browser, Selector


class DataObjectTypeSelector(Selector):
    def __init__(self, storage_account_manager: StorageAccountManager):
        self.storage_account_manager = storage_account_manager
        super().__init__()

    def iter_options(self):
        yield ("container", "Containers")
        yield ("table", "Tables")

    def get_option_widget(self, id_):
        if id_ == "container":
            return ContainerExplorer(self.storage_account_manager)
        elif id_ == "table":
            return TableExplorer(self.storage_account_manager)
        else:
            raise ValueError(f"Unknown data object type: {id_}")


class ContainerExplorer(Browser):
    COLUMN_NAMES = ["Name"]

    def __init__(self, storage_account_manager: StorageAccountManager):
        self.storage_account_manager = storage_account_manager
        super().__init__()

    def check_valid(self) -> bool:
        self.storage_account_manager.check_access("container")

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for container_name in self.storage_account_manager.list_container_names():
            yield container_name, (f"📁 {container_name}",)

    def get_item_widget(self, item: str) -> Widget:
        container_manager = self.storage_account_manager.get_container_manager(
            container_name=item,
        )
        return BlobFolderBrowser(container_manager)


class TableExplorer(Browser):
    COLUMN_NAMES = ["Name"]

    def __init__(self, storage_account_manager: StorageAccountManager):
        self.storage_account_manager = storage_account_manager
        super().__init__()

    def check_valid(self) -> bool:
        self.storage_account_manager.check_access("table")

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for table_name in self.storage_account_manager.list_table_names():
            yield table_name, (f"📅 {table_name}",)
