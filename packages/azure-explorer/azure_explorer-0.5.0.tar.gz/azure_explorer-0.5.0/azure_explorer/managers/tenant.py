from azure.core.credentials import TokenCredential
from azure.mgmt.subscription import SubscriptionClient

from azure_explorer.managers.base import Manager
from azure_explorer.managers.models import SubscriptionProperties
from azure_explorer.managers.subscription import SubscriptionManager


class TenantManager(Manager):
    def __init__(self, credential: TokenCredential):
        self.sub_client = SubscriptionClient(credential)
        self.credential = credential

    def check_access(self) -> bool:
        next(self.sub_client.subscriptions.list())

    def list_subscriptions(self) -> list[SubscriptionProperties]:
        items = []
        for sub in self.sub_client.subscriptions.list():
            item = SubscriptionProperties(
                sub.subscription_id,
                sub.display_name,
            )
            items.append(item)
        return items

    def list_subscription_ids(self) -> list[str]:
        return [item.id for item in self.list_subscriptions()]

    def list_subscription_names(self) -> list[str]:
        return [item.name for item in self.list_subscriptions()]

    def get_subscription_manager(self, subscription_id: str):
        return SubscriptionManager(subscription_id, self.credential)

    def __repr__(self) -> str:
        return "TenantManager()"
