import json
import unittest
import os

from mock import patch, call

from mailgunsdk.api import MailgunApi
from mailgunsdk.domain.messages import Messages


class MessagesTestCase(unittest.TestCase):
    def setUp(self):
        super(MessagesTestCase, self).setUp()
        api = MailgunApi(api_key="blah")
        self.messages = Messages(api, api.domain('blah.net'), os.getenv('MAILGUN_BASE_URL'))

    @patch.object(Messages, "request")
    def test_send_via_template(self, request):
        sending_variables = {"title": "API documentation", "body": "Sending messages with templates"}
        
        self.messages.send_via_template(
            from_name="Al brenss",
            from_email="albrens@domain.com",
            to="ml@domain.com",
            subject="Hello",
            template="template.test",
            variables=sending_variables
        )

        request.assert_called_with(
            "POST",
            data={
                "from": "Al brenss <albrens@domain.com>",
                "to": ["ml@domain.com"],
                "subject": "Hello",
                "template": "template.test",
                "h:X-Mailgun-Variables": json.dumps(
                    sending_variables
                )
            },
        )

    @patch.object(Messages, "request")
    def test_send_with_tls(self, request):
        sending_variables = {"title": "API documentation", "body": "Sending messages with templates"}
        self.messages.require_tls = True
        self.messages.send_via_template(
            from_name="Al brenss",
            from_email="albrens@domain.com",
            to="ml@domain.com",
            subject="Hello",
            template="template.test",
            variables=sending_variables
        )

        request.assert_called_with(
            "POST",
            data={
                "from": "Al brenss <albrens@domain.com>",
                "to": ["ml@domain.com"],
                "subject": "Hello",
                "template": "template.test",
                "h:X-Mailgun-Variables": json.dumps(
                    sending_variables
                ),
                "o:require-tls": "True"
            },
        )
