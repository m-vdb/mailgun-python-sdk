import json
import unittest

from mock import patch

from mailgun.api import MailgunApi
from mailgun.ips import IPs


class IPsTestCase(unittest.TestCase):

    def setUp(self):
        super(IPsTestCase, self).setUp()
        self.ips = IPs(MailgunApi())

    @patch.object(IPs, 'request')
    def test_list(self, request):
        response = self.ips.list()

        request.assert_called_with(
            'GET',
            params={}
        )
        self.assertEqual(response, request.return_value)

    @patch.object(IPs, 'request')
    def test_list_dedicated(self, request):
        response = self.ips.list(True)

        request.assert_called_with(
            'GET',
            params={'dedicated': 'true'}
        )
        self.assertEqual(response, request.return_value)

    @patch.object(IPs, 'request')
    def test_detail(self, request):
        response = self.ips.detail('111.222.333.444')

        request.assert_called_with(
            'GET',
            '111.222.333.444'
        )
        self.assertEqual(response, request.return_value)
