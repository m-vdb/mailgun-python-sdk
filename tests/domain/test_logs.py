import unittest

from mock import patch

from mailgun.api import MailgunApi
from mailgun.domain.logs import Logs


api = MailgunApi()


class LogsTestCase(unittest.TestCase):

    def setUp(self):
        super(LogsTestCase, self).setUp()
        self.logs = Logs(api, api.domain('mydomain.com'))

    @patch.object(Logs, 'request')
    def test_list(self, request):
        response = self.logs.list()

        request.assert_called_with(
            'GET',
            params={
                'limit': 300,
                'skip': 0,
            }
        )
        self.assertEqual(response, request.return_value)

    @patch.object(Logs, 'request')
    def test_list_parameters(self, request):
        response = self.logs.list(42, 84)

        request.assert_called_with(
            'GET',
            params={
                'limit': 42,
                'skip': 84,
            }
        )
        self.assertEqual(response, request.return_value)
