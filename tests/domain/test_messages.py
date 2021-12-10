import json
import unittest

from mock import patch, call

from mailgun.api import MailgunApi
from mailgun.domain.messages import Messages


class MailingListTestCase(unittest.TestCase):
    def setUp(self):
        super(MailingListTestCase, self).setUp()
        api = MailgunApi(api_key="blah")
        self.messages = Messages(api, api.domain("blah.net"))

    @patch.object(Messages, "request")
    def test_send_via_template(self, request):
        sending_vars = {"title": "API documentation", "body": "Sending messages with templates"}
        self.messages.send_via_template(
            from_name="Al brenss",
            from_email="albrens@domain.com",
            to="ml@domain.com",
            subject="Hello",
            template="template.test",
            vars=sending_vars
        )

        request.assert_called_with(
            "POST",
            data={
                "from": "Al brenss <albrens@domain.com>",
                "to": ["ml@domain.com"],
                "subject": "Hello",
                "template": "template.test",
                "h:X-Mailgun-Variables": json.dumps(
                    sending_vars
                )
            },
        )
