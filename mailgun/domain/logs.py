"""Logs API."""
from ..base import ApiDomainResource


class Logs(ApiDomainResource):
    """
    Logs resource.
    """
    api_endpoint = 'log'

    def list(self, limit=300, offset=0):
        """
        List the logs.
        """
        return self.request('GET', params={'limit': limit, 'skip': offset})
