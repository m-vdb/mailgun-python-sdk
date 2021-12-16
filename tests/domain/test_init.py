import unittest

from mailgun_sdk.api import MailgunApi
from mailgun_sdk.domain import Domain
from mailgun_sdk.domain.logs import Logs

api = MailgunApi()


class DomainTestCase(unittest.TestCase):
    def test_init(self):
        domain = Domain(api, "mydomain.com")
        self.assertEqual(domain.api, api)
        self.assertEqual(domain.name, "mydomain.com")
        self.assertIsInstance(domain.logs, Logs)
        self.assertIs(domain.logs.api, api)
        self.assertIs(domain.logs.domain, domain)
