"""Base classes and functions."""


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
