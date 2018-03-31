"""IPs API."""
from .base import ApiResource


class IPs(ApiResource):
    """
    IPs resource.
    """
    api_endpoint = 'ips'

    def list(self, dedicated=False):
        """
        List the existing IPs.
        """
        params = {}
        if dedicated:
            params['dedicated'] = 'true'
        return self.request('GET', params=params)

    def detail(self, ip):  # pylint: disable=invalid-name
        """
        Get detail information about an IP.

        :param ip:           the ip address
        """
        return self.request('GET', ip)
