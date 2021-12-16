import unittest

import mailgun_sdk
from mailgun_sdk.api import MailgunApi


class MailgunInitTestCase(unittest.TestCase):
    def test_api(self):
        self.assertIsInstance(mailgun_sdk.api, MailgunApi)

    def test_initialize(self):
        mailgun_sdk.initialize("api-key-xxx")
        self.assertEqual(mailgun_sdk.api.api_key, "api-key-xxx")
