import unittest

from mock import patch

from mailgun.api import MailgunApi
from mailgun.base import ApiResource


class FakeResource(ApiResource):
    api_endpoint = 'fake'


api = MailgunApi()


class ApiResourceTestCase(unittest.TestCase):

    def test_init_no_endpoint(self):
        with self.assertRaisesRegexp(AssertionError, 'Missing'):
            ApiResource(api)

    def test_init_ok(self):
        resource = FakeResource(api)
        self.assertEqual(resource.api, api)
        self.assertEqual(resource.base_url, 'https://api.mailgun.net/v3/fake')

    @patch('requests.Session.request')
    def test_request(self, request):
        resource = FakeResource(api)
        response = resource.request('POST')

        request.assert_called_with('POST', resource.base_url)
        request.return_value.raise_for_status.assert_called_with()
        request.return_value.json.assert_called_with()
        self.assertEqual(response, request.return_value.json.return_value)

    @patch('requests.Session.request')
    def test_request_with_additional_endpoint(self, request):
        resource = FakeResource(api)
        response = resource.request('POST', 'do-stuff')

        request.assert_called_with('POST', 'https://api.mailgun.net/v3/fake/do-stuff')
        request.return_value.raise_for_status.assert_called_with()
        request.return_value.json.assert_called_with()
        self.assertEqual(response, request.return_value.json.return_value)

    @patch('requests.Session.request')
    def test_request_with_params(self, request):
        resource = FakeResource(api)
        response = resource.request('POST', some_value='stuff')

        request.assert_called_with('POST', resource.base_url, some_value='stuff')
        request.return_value.raise_for_status.assert_called_with()
        request.return_value.json.assert_called_with()
        self.assertEqual(response, request.return_value.json.return_value)
