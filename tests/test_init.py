import unittest

import mailgunsdk
from mailgunsdk.api import MailgunApi


class MailgunInitTestCase(unittest.TestCase):
    def test_api(self):
        self.assertIsInstance(mailgunsdk.api, MailgunApi)

    def test_initialize(self):
        mailgunsdk.initialize("api-key-xxx")
        self.assertEqual(mailgunsdk.api.api_key, "api-key-xxx")
