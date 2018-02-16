from __future__ import unicode_literals
import unittest

from mock import patch
from requests import Response
from requests.exceptions import HTTPError

from mailgun.api import MailgunApi
from mailgun.base import ApiResource, silence_error


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

    def test_silence_error_no_error(self):
        @silence_error(400, 'stuff')
        def func():
            return 'response'

        self.assertEqual(func(), 'response')

    def test_silence_error_is_not_httperror(self):
        @silence_error(400, 'stuff')
        def func():
            raise ValueError('oups')

        with self.assertRaisesRegexp(ValueError, 'oups'):
            func()

    def test_silence_error_different_status_code(self):
        @silence_error(400, 'stuff')
        def func():
            resp = Response()
            resp.status_code = 404
            raise HTTPError(response=resp)

        with self.assertRaises(HTTPError):
            func()

    def test_silence_error_response_is_not_json(self):
        @silence_error(400, 'stuff')
        def func():
            resp = Response()
            resp.status_code = 400
            resp._content = 'something not json'.encode('utf-8')
            resp.encoding = 'utf-8'
            raise HTTPError(response=resp)

        with self.assertRaises(HTTPError):
            func()

    def test_silence_error_body_doesnt_match(self):
        @silence_error(400, 'stuff')
        def func():
            resp = Response()
            resp.status_code = 400
            resp._content = '{"message": "other"}'.encode('utf-8')
            resp.encoding = 'utf-8'
            raise HTTPError(response=resp)

        with self.assertRaises(HTTPError):
            func()

    def test_silence_error_caught_and_returns_body(self):
        @silence_error(400, 'stuff')
        def func():
            resp = Response()
            resp.status_code = 400
            resp._content = '{"message": "some stuff happened"}'.encode('utf-8')
            resp.encoding = 'utf-8'
            raise HTTPError(response=resp)

        self.assertEqual(func(), {"message": "some stuff happened"})
