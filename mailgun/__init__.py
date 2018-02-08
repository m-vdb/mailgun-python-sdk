"""Mailgun module."""
from .api import MailgunApi


api = MailgunApi()


def initialize(api_key):
    """
    Initialize the default api.
    """
    api.set_api_key(api_key)
