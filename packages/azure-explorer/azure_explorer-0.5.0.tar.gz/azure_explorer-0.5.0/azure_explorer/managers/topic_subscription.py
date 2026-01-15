from typing import Iterator

from azure.core.credentials import TokenCredential
from azure.servicebus import ServiceBusClient, ServiceBusSubQueue
from azure.servicebus.management import ServiceBusAdministrationClient

from azure_explorer.managers.base import Manager
from azure_explorer.managers.models import MessageProperties

PEEK_MESSAGE_BATCH_SIZE = 10


class TopicSubscriptionManager(Manager):
    def __init__(
        self,
        service_bus_name: str,
        topic_name: str,
        subscription_name: str,
        credential: TokenCredential,
    ):
        self.service_bus_name = service_bus_name
        self.credential = credential
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.service_bus_client = ServiceBusClient(
            fully_qualified_namespace=f"{service_bus_name}.servicebus.windows.net",
            credential=credential,
        )
        self.service_bus_adm_client = ServiceBusAdministrationClient(
            fully_qualified_namespace=f"{service_bus_name}.servicebus.windows.net",
            credential=credential,
        )
        self.runtime_properties = (
            self.service_bus_adm_client.get_subscription_runtime_properties(
                self.topic_name, self.subscription_name
            )
        )

    def check_access(self) -> bool:
        receiver = self.service_bus_client.get_subscription_receiver(
            self.topic_name, self.subscription_name
        )
        receiver.peek_messages(max_message_count=1)

    def num_active_messages(self):
        return self.runtime_properties.active_message_count

    def num_deadletter_messages(self):
        return self.runtime_properties.dead_letter_message_count

    def _iter_sub_queue_messages(self, sub_queue) -> list[MessageProperties]:
        receiver = self.service_bus_client.get_subscription_receiver(
            self.topic_name, self.subscription_name, sub_queue=sub_queue
        )
        seq_num = 0
        # iterate in batches of PEEK_MESSAGE_BATCH_SIZE
        while True:
            empty_batch = True
            for msg in receiver.peek_messages(
                max_message_count=PEEK_MESSAGE_BATCH_SIZE,
                sequence_number=seq_num,
            ):
                empty_batch = False
                yield MessageProperties(
                    id=msg.message_id,
                    subject=msg.subject,
                )
                seq_num = msg.sequence_number + 1

            if empty_batch:
                break

    def iter_active_messages(self) -> Iterator[MessageProperties]:
        yield from self._iter_sub_queue_messages(sub_queue=None)

    def list_active_messages(self) -> list[MessageProperties]:
        return list(self.iter_active_messages())

    def iter_deadletter_messages(self) -> Iterator[MessageProperties]:
        yield from self._iter_sub_queue_messages(
            sub_queue=ServiceBusSubQueue.DEAD_LETTER
        )

    def list_deadletter_messages(self) -> list[MessageProperties]:
        return list(self.iter_deadletter_messages())
