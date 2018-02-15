import unittest

import requests

from mailgun.api import MailgunApi
from mailgun.mailing_list import MailingList


class MailgunApiTestCase(unittest.TestCase):

    def test_init(self):
        api = MailgunApi()
        self.assertIsNone(api.api_key)
        self.assertIsInstance(api.session, requests.Session)
        self.assertIsInstance(api.mailing_list, MailingList)
        self.assertIs(api.mailing_list.api, api)

    def test_set_api_key(self):
        api = MailgunApi()
        api.set_api_key('api-key-xxx')
        self.assertEqual(api.api_key, 'api-key-xxx')
        self.assertEqual(api.session.auth, ('api', 'api-key-xxx'))
