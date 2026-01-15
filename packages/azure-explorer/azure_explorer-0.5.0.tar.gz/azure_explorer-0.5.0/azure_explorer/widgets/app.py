from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from azure_explorer.config import Config
from azure_explorer.managers import TenantManager
from azure_explorer.widgets.components import SubscriptionBrowser


class AzureExplorerApp(App):

    BINDINGS = [
        Binding("ctrl+x", "quit", "Exit", show=True, priority=True),
    ]

    TITLE = "Azure Explorer"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self):
        tenant_manager = TenantManager(credential=Config.credential)
        try:
            tenant_manager.check_access()
        except Exception as exc:
            self.notify(str(exc), severity="error")
            return

        sub_browser = SubscriptionBrowser(tenant_manager)
        self.mount(sub_browser)


def run():
    AzureExplorerApp().run()
