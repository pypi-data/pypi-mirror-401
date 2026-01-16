from typing import Iterator

from textual.widget import Widget

from azure_explorer.managers import TenantManager
from azure_explorer.widgets.components.azure.subscription import ResourceTypeSelector
from azure_explorer.widgets.components.windows import Browser


class SubscriptionBrowser(Browser):
    COLUMN_NAMES = ["Name", "ID"]

    def __init__(self, tenant_manager: TenantManager):
        self.tenant_manager = tenant_manager
        super().__init__()

    def check_valid(self):
        self.tenant_manager.check_access()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for subscription in self.tenant_manager.list_subscriptions():
            yield subscription.id, (subscription.name, subscription.id)

    def get_item_widget(self, id_: str) -> Widget:
        subscription_manager = self.tenant_manager.get_subscription_manager(
            subscription_id=id_,
        )
        return ResourceTypeSelector(subscription_manager)
