from pathlib import Path
from typing import Iterator

from textual.binding import Binding
from textual.widget import Widget

from azure_explorer.config import Config
from azure_explorer.managers import ContainerManager
from azure_explorer.widgets.components.windows import Browser

READ_FILE_CODE_SNIPPET = """
import azure_explorer as ax

ax.read_file(
    storage_account_name="{self.container_manager.storage_account_name}",
    container_name="{self.container_manager.container_name}",
    path="{item}",
)
"""


class BlobFolderBrowser(Browser):
    COLUMN_NAMES = ["Name", "Size (MB)", "Last Modified", "Created Time"]

    BINDINGS = [
        Binding("ctrl+s", "download", "Download", show=True, priority=True),
        Binding("ctrl+c", "copy_code", "Copy code", show=True, priority=True),
    ]

    def __init__(self, container_manager: ContainerManager, folder: str = ""):
        self.container_manager = container_manager
        self.folder = folder
        super().__init__()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "copy_code":
            item = self.get_highlighted_item()
            if self.container_manager.is_dir(item):
                return None
        return super().check_action(action, parameters)

    def action_download(self):
        id_ = self.get_highlighted_item()

        path = f"{self.folder}/{id_}" if self.folder else id_

        download_folder = Path.cwd() / ".downloads" / path

        if self.container_manager.is_dir(path):
            self.container_manager.download_dir(path, download_folder)
        else:
            self.container_manager.download_file(path, download_folder)

    def action_copy_code(self):
        item = self.get_highlighted_item()
        code_snippet = READ_FILE_CODE_SNIPPET.format(
            self=self,
            item=item,
        )
        self.app.copy_to_clipboard(code_snippet)
        self.notify("Code snippet copied to clipboard!", severity="info", timeout=3)

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for subitem in self.container_manager.iter_dir(self.folder):
            if self.container_manager.is_dir(subitem.path):
                icon = "📁"
            else:
                icon = "📄"

            if subitem.path.endswith("/"):
                base_name = subitem.path
            else:
                base_name = subitem.path.split("/")[-1]

            if subitem.last_modified_time:
                last_modified_time_local = subitem.last_modified_time.astimezone(
                    Config.time_zone
                )
            else:
                last_modified_time_local = "-"

            if subitem.created_time:
                created_time_local = subitem.created_time.astimezone(Config.time_zone)
            else:
                created_time_local = "-"

            if subitem.size:
                size_MB = round(subitem.size / (1024 * 1024), 2)
            else:
                size_MB = "-"

            yield base_name, (
                f"{icon} {base_name}",
                size_MB,
                last_modified_time_local,
                created_time_local,
            )

    def get_item_widget(self, id_: str) -> Widget:
        path = f"{self.folder.rstrip('/')}/{id_}" if self.folder else id_

        if not self.container_manager.is_dir(path):
            return

        return BlobFolderBrowser(
            self.container_manager,
            path,
        )
