from azure.core.credentials import TokenCredential
from azure.servicebus.management import ServiceBusAdministrationClient

from azure_explorer.managers import utils
from azure_explorer.managers.base import Manager
from azure_explorer.managers.models import TopicProperties
from azure_explorer.managers.topic import TopicManager


class ServiceBusManager(Manager):
    def __init__(self, service_bus_name: str, credential: TokenCredential):
        self.service_bus_name = service_bus_name
        self.credential = credential
        self.fully_qualified_namespace = f"{service_bus_name}.servicebus.windows.net"
        self.service_bus_adm_client = ServiceBusAdministrationClient(
            self.fully_qualified_namespace,
            credential,
        )

    def get_topic_manager(self, topic_name: str) -> TopicManager:
        return TopicManager(self.service_bus_name, topic_name, self.credential)

    def check_access(self) -> bool:
        utils.check_connection(self.fully_qualified_namespace)
        next(self.service_bus_adm_client.list_topics_runtime_properties())

    def list_topics(self) -> list[TopicProperties]:
        topics = []
        for (
            topic_runtime_props
        ) in self.service_bus_adm_client.list_topics_runtime_properties():
            topic = TopicProperties(
                name=topic_runtime_props.name,
            )
            topics.append(topic)
        return topics

    def list_topic_names(self) -> list[str]:
        return [topic.name for topic in self.list_topics()]

    def list_queue_names(self) -> list[str]:
        return [queue.name for queue in self.service_bus_adm_client.list_queues()]

    def __repr__(self) -> str:
        return f"ServiceBusManager(service_bus_name={self.service_bus_name})"
