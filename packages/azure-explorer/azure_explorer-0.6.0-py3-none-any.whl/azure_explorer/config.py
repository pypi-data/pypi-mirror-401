import pytz
from azure.identity import DefaultAzureCredential


class Config:
    credential = DefaultAzureCredential()
    time_zone = pytz.timezone("Europe/Copenhagen")
