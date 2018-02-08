"""Mailgun client module."""
import requests

from .mailing_list import MailingList


class MailgunApi(object):  # pylint: disable=too-few-public-methods
    """
    Mailgun API client.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        # APIs
        self.mailing_list = MailingList(self)

    def set_api_key(self, api_key):
        """
        Set the API key on the client. This is called by `mailgun.initialize()`.

        :param api_key:         your Mailgun API key
        """
        self.api_key = api_key
        self.session.auth = ('api', api_key)
