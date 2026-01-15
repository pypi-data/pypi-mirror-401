from typing import Iterator, Literal

from textual.widget import Widget

from azure_explorer.managers import (
    ServiceBusManager,
    TopicManager,
    TopicSubscriptionManager,
)
from azure_explorer.widgets.components.windows import Browser, Selector


class EntitySelector(Selector):
    def __init__(self, sb_manager: ServiceBusManager):
        self.sb_manager = sb_manager
        super().__init__()

    def iter_options(self):
        yield ("topic", "Topics")
        yield ("queue", "Queues")

    def get_option_widget(self, id_):
        if id_ == "topic":
            return TopicExplorer(self.sb_manager)


class TopicExplorer(Browser):
    COLUMN_NAMES = ["Name"]

    def __init__(self, sb_manager: ServiceBusManager):
        self.sb_manager = sb_manager
        super().__init__()

    def check_valid(self) -> bool:
        self.sb_manager.check_access()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for topic in self.sb_manager.list_topics():
            yield topic.name, (topic.name,)

    def get_item_widget(self, item: str) -> Widget:
        topic_manager = self.sb_manager.get_topic_manager(
            topic_name=item,
        )
        return TopicSubscriptionExplorer(topic_manager)


class TopicSubscriptionExplorer(Browser):
    COLUMN_NAMES = ["Name", "Active Messages", "Dead-letter Messages"]

    def __init__(self, topic_manager: TopicManager):
        self.topic_manager = topic_manager
        super().__init__()

    def check_valid(self):
        return self.topic_manager.check_access()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        for sub in self.topic_manager.list_subscription():
            yield sub.name, (
                sub.name,
                sub.num_active_messages,
                sub.num_deadletter_messages,
            )

    def get_item_widget(self, id_: str) -> Widget:
        subscription_manager = self.topic_manager.get_subscription_manager(
            subscription_name=id_,
        )

        return SubQueueSelector(subscription_manager)


class SubQueueSelector(Selector):
    def __init__(self, subscription_manager: TopicSubscriptionManager):
        self.subscription_manager = subscription_manager
        super().__init__()

    def iter_options(self):
        yield ("active", "Active Messages")
        yield ("deadletter", "Dead-letter Messages")

    def get_option_widget(self, id_):
        return MessageSubjectExplorer(
            self.subscription_manager,
            id_,
        )


class MessageSubjectExplorer(Browser):
    COLUMN_NAMES = ["Subject"]

    def __init__(
        self,
        subscription_manager: TopicSubscriptionManager,
        sub_queue: Literal["active", "deadletter"],
    ):
        self.subscription_manager = subscription_manager
        self.sub_queue = sub_queue
        super().__init__()

    def check_valid(self):
        return self.subscription_manager.check_access()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        found_subjects = []

        if self.sub_queue == "deadletter":
            messages = self.subscription_manager.iter_deadletter_messages()
        elif self.sub_queue == "active":
            messages = self.subscription_manager.iter_active_messages()
        else:
            raise ValueError(f"Unknown sub-queue `{self.sub_queue}`")

        for message in messages:
            if message.subject in found_subjects:
                continue
            yield message.subject, (message.subject,)
            found_subjects.append(message.subject)

    def get_item_widget(self, id_: str) -> Widget:
        return MessageExplorer(
            self.subscription_manager,
            self.sub_queue,
            id_,
        )


class MessageExplorer(Browser):
    COLUMN_NAMES = ["Message ID", "Subject"]

    def __init__(
        self,
        subscription_manager: TopicSubscriptionManager,
        sub_queue: Literal["active", "deadletter"],
        subject: str,
    ):
        self.subscription_manager = subscription_manager
        self.sub_queue = sub_queue
        self.subject = subject
        super().__init__()

    def iter_rows(self) -> Iterator[tuple[str, tuple]]:
        if self.sub_queue == "deadletter":
            messages = self.subscription_manager.iter_deadletter_messages()
        else:
            messages = self.subscription_manager.iter_active_messages()

        for message in messages:
            if message.subject == self.subject:
                yield message.id, (message.id, message.subject)
