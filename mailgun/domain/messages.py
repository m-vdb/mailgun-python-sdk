"""
Messages API.
url: https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-api
"""
from __future__ import division
import json
import math

from mailgun.base import ApiDomainResource


class Messages(ApiDomainResource):
    """
    Mailing list resource.
    """

    api_endpoint = "messages"
    require_tls = False
    """
    data example
    data={
                "from": "Excited User <YOU@YOUR_DOMAIN_NAME>",
                "to": ["bar@example.com"],
                "subject": "Hello",
                "template": "template.test",
                "h:X-Mailgun-Variables": json.dumps(
                      {"title": "API documentation", "body": "Sending messages with templates"}
                )
            },
    """

    def send_via_template(self, from_name: str, from_email: str, to: str, subject: str, template: str, variables: dict):
        payload = {
            "from": "{} <{}>".format(from_name, from_email),
            "to": [to],
            "subject": subject,
            "template": template,
            "h:X-Mailgun-Variables": json.dumps(variables)
        }

        if self.require_tls:
            payload['o:require-tls'] = 'True'

        return self.request(
            "POST",
            data=payload,
        )
