class AccessError(Exception):
    pass


class ConnectionError(AccessError):
    def __init__(self, url: str):
        self.url = url
        super().__init__(
            f"Unable to connect to '{url}'. Are you working in a VNET, then remember "
            "to add a private endpoint for this resource."
        )


class AuthorizationError(AccessError):
    pass
