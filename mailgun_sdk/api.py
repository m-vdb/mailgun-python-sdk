"""Mailgun client module."""
from functools import partial

import requests

from .domain import Domain
from .ips import IPs
from .mailing_list import MailingList


class MailgunApi(object):  # pylint: disable=too-few-public-methods
    """
    Mailgun API client.
    """

    def __init__(self, api_key=None):
        self.session = requests.Session()
        self.set_api_key(api_key)

        # APIs
        self.ips = IPs(self)
        self.mailing_list = MailingList(self)
        # Domain APIs
        self.domain = partial(Domain, self)

    def set_api_key(self, api_key):
        """
        Set the API key on the client. This is called by `mailgun_sdk.initialize()`.

        :param api_key:         your Mailgun API key
        """
        self.api_key = api_key
        self.session.auth = ("api", api_key)
