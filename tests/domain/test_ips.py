import unittest

from mock import patch

from mailgun.api import MailgunApi
from mailgun.domain.ips import IPs


api = MailgunApi()


class IPsTestCase(unittest.TestCase):

    def setUp(self):
        super(IPsTestCase, self).setUp()
        self.ips = IPs(api, api.domain('mydomain.com'))

    @patch.object(IPs, 'request')
    def test_create(self, request):
        response = self.ips.create('111.222.333.444')

        request.assert_called_with(
            'POST',
            data={'ip': '111.222.333.444'}
        )
        self.assertEqual(response, request.return_value)

    @patch.object(IPs, 'request')
    def test_list(self, request):
        response = self.ips.list()

        request.assert_called_with(
            'GET'
        )
        self.assertEqual(response, request.return_value)

    @patch.object(IPs, 'request')
    def test_delete(self, request):
        response = self.ips.delete('111.222.333.444')

        request.assert_called_with(
            'DELETE',
            '111.222.333.444'
        )
        self.assertEqual(response, request.return_value)
