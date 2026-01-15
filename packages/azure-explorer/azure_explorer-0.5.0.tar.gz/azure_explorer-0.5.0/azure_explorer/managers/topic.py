from azure.core.credentials import TokenCredential
from azure.servicebus.management import ServiceBusAdministrationClient

from azure_explorer.managers.base import Manager
from azure_explorer.managers.models import TopicSubscriptionProperties
from azure_explorer.managers.topic_subscription import TopicSubscriptionManager


class TopicManager(Manager):
    def __init__(
        self, service_bus_name: str, topic_name: str, credential: TokenCredential
    ):
        self.service_bus_name = service_bus_name
        self.credential = credential
        self.topic_name = topic_name
        self.service_bus_adm_client = ServiceBusAdministrationClient(
            fully_qualified_namespace=f"{service_bus_name}.servicebus.windows.net",
            credential=credential,
        )

    def check_access(self) -> bool:
        next(
            self.service_bus_adm_client.list_subscriptions_runtime_properties(
                self.topic_name
            )
        )

    def list_subscription(self) -> list[TopicSubscriptionProperties]:
        subscriptions = []
        for (
            sub_runtime_props
        ) in self.service_bus_adm_client.list_subscriptions_runtime_properties(
            self.topic_name
        ):
            subscription = TopicSubscriptionProperties(
                name=sub_runtime_props.name,
                num_active_messages=sub_runtime_props.active_message_count,
                num_deadletter_messages=sub_runtime_props.dead_letter_message_count,
            )
            subscriptions.append(subscription)
        return subscriptions

    def list_subscription_names(self) -> list[str]:
        return [sub.name for sub in self.list_subscription()]

    def get_subscription_manager(
        self,
        subscription_name: str,
    ) -> TopicSubscriptionManager:
        return TopicSubscriptionManager(
            self.service_bus_name,
            self.topic_name,
            subscription_name,
            self.credential,
        )
