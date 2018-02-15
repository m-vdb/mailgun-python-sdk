import unittest

import mailgun
from mailgun.api import MailgunApi


class MailgunInitTestCase(unittest.TestCase):

    def test_api(self):
        self.assertIsInstance(mailgun.api, MailgunApi)

    def test_initialize(self):
        mailgun.initialize('api-key-xxx')
        self.assertEqual(mailgun.api.api_key, 'api-key-xxx')
