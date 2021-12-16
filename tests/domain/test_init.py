import unittest

from mailgunsdk.api import MailgunApi
from mailgunsdk.domain import Domain
from mailgunsdk.domain.logs import Logs

api = MailgunApi()


class DomainTestCase(unittest.TestCase):
    def test_init(self):
        domain = Domain(api, "mydomain.com")
        self.assertEqual(domain.api, api)
        self.assertEqual(domain.name, "mydomain.com")
        self.assertIsInstance(domain.logs, Logs)
        self.assertIs(domain.logs.api, api)
        self.assertIs(domain.logs.domain, domain)
