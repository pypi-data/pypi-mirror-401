import socket

from azure_explorer.managers.exceptions import ConnectionError


def check_connection(url: str):
    try:
        socket.getaddrinfo(url, 443)
    except socket.gaierror:
        raise ConnectionError(url)
