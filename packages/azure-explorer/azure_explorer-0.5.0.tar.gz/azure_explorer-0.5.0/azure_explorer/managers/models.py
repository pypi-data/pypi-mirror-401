import datetime as dt
from dataclasses import dataclass, field


@dataclass
class ServiceBusProperties:
    name: str


@dataclass
class SubscriptionProperties:
    id: str = field(repr=False)
    name: str


@dataclass
class StorageAccountProperties:
    name: str
    is_data_lake: bool


@dataclass
class TopicProperties:
    name: str


@dataclass
class TopicSubscriptionProperties:
    name: str
    num_active_messages: int = field(default=None)
    num_deadletter_messages: int = field(default=None)


@dataclass
class FileProperties:
    path: str
    size: float
    last_modified_time: dt.datetime
    created_time: dt.datetime


@dataclass
class FolderProperties:
    path: str
    size: float
    last_modified_time: dt.datetime
    created_time: dt.datetime


@dataclass
class MessageProperties:
    id: str
    subject: str
