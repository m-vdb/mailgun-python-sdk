"""Base classes and functions."""
import functools
import re
import sys

from requests.exceptions import HTTPError
import six


class ApiResource(object):  # pylint: disable=too-few-public-methods
    """
    Base class for API resource.
    """
    api_endpoint = None
    api_url = 'https://api.mailgun.net/v3'

    def __init__(self, api):
        assert self.api_endpoint, 'Missing `api_endpoint` attribute definition.'
        self.base_url = '{}/{}'.format(self.api_url, self.api_endpoint)
        self.api = api

    def request(self, method, endpoint='', **params):
        """
        Perform a request using the api session.

        :param method:              HTTP verb
        :param endpoint:            additional enpoint on the API
        :param **params:            every additional keyword argument is
                                    forwarded to `requests`
        """
        url = self.base_url
        if endpoint:
            url = '{}/{}'.format(url, endpoint)

        response = self.api.session.request(method, url, **params)
        response.raise_for_status()

        return response.json()


def silence_error(status_code, msg_pattern):
    """
    A decorator to silence errors during an API call. For instance
    removing an address from a mailing list shouldn't yield to an error
    in case the address is not present in the mailing list.

    :param status_code:          the status code to catch
    :param msg_pattern:          a pattern to match the body message
    """

    def decorator(func):
        """
        Actual decorator.
        """

        @functools.wraps(func)
        def inner(*args, **kwargs):
            """
            Inner wrapper for the function.
            """
            try:
                return func(*args, **kwargs)
            except HTTPError as exc:
                exc_info = sys.exc_info()
                if exc.response.status_code == status_code:
                    try:
                        response = exc.response.json()
                    except ValueError:
                        pass
                    else:
                        if re.search(msg_pattern, response.get('message', '')):
                            return response
                six.reraise(*exc_info)

        return inner

    return decorator
