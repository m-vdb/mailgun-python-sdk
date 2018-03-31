"""IPs domain API."""
from ..base import ApiDomainResource


class IPs(ApiDomainResource):
    """
    IPs domain resource.
    """
    api_endpoint = 'ips'
    DOMAIN_NAMESPACE = True

    def list(self):
        """
        List the existing IPs on the domain.
        """
        return self.request('GET')

    def create(self, ip):  # pylint: disable=invalid-name
        """
        Assign a dedicated IP to the domain.

        :param ip:                 the new IP address to assign
        """
        return self.request('POST', data={'ip': ip})

    def delete(self, ip):  # pylint: disable=invalid-name
        """
        Delete an existing IP on a domain.
        """
        return self.request('DELETE', ip)
