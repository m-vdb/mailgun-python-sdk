"""Domain API. Will contain all APIs that are domain-based."""
from .logs import Logs


class Domain(object):  # pylint: disable=too-few-public-methods
    """
    Domain resource. It handles the Domain API and every
    underlying API that relies on domains.
    """

    def __init__(self, api, name):
        self.api = api
        self.name = name
        self.logs = Logs(api, self)
