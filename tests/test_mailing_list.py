import json
import unittest

from mock import patch, call

from mailgun.api import MailgunApi
from mailgun.mailing_list import MailingList


class MailingListTestCase(unittest.TestCase):
    def setUp(self):
        super(MailingListTestCase, self).setUp()
        self.mailing_list = MailingList(MailgunApi())

    @patch.object(MailingList, "request")
    def test_create(self, request):
        response = self.mailing_list.create(
            "ml@domain.com", description="A mailing list"
        )

        request.assert_called_with(
            "POST",
            data={
                "address": "ml@domain.com",
                "name": None,
                "description": "A mailing list",
                "access_level": None,
            },
        )
        self.assertEqual(response, request.return_value)

    @patch.object(MailingList, "request")
    def test_list(self, request):
        response = self.mailing_list.list()

        request.assert_called_with("GET")
        self.assertEqual(response, request.return_value)

    @patch.object(MailingList, "request")
    def test_delete(self, request):
        response = self.mailing_list.delete("ml@domain.com")

        request.assert_called_with("DELETE", "ml@domain.com")
        self.assertEqual(response, request.return_value)

    @patch.object(MailingList, "request")
    def test_add_list_member(self, request):
        response = self.mailing_list.add_list_member(
            "ml@domain.com", "member@gmail.com", {"key": "value"}, name="John"
        )

        request.assert_called_with(
            "POST",
            "ml@domain.com/members",
            data={
                "subscribed": True,
                "address": "member@gmail.com",
                "name": "John",
                "vars": '{"key": "value"}',
            },
        )
        self.assertEqual(response, request.return_value)

    @patch.object(MailingList, "request")
    def test_update_list_member(self, request):
        response = self.mailing_list.update_list_member(
            "ml@domain.com",
            "member@gmail.com",
            parameters={"key": "value"},
            subscribed=True,
        )

        request.assert_called_with(
            "PUT",
            "ml@domain.com/members/member@gmail.com",
            data={"subscribed": True, "name": None, "vars": '{"key": "value"}'},
        )
        self.assertEqual(response, request.return_value)

    @patch.object(MailingList, "request")
    def test_update_multiple_list_members(self, request):
        responses = self.mailing_list.update_multiple_list_members(
            "ml@domain.com",
            [
                "member1@gmail.com",
                {"address": "member2@gmail.com", "subscribed": False},
            ],
        )

        members_data = json.dumps(
            ["member1@gmail.com", {"address": "member2@gmail.com", "subscribed": False}]
        )
        request.assert_called_with(
            "POST",
            "ml@domain.com/members.json",
            data={"members": members_data, "upsert": "no"},
        )
        self.assertEqual(responses, [request.return_value])

    @patch.object(MailingList, "request")
    def test_update_multiple_list_members_upsert(self, request):
        responses = self.mailing_list.update_multiple_list_members(
            "ml@domain.com", ["member1@gmail.com"], True
        )

        request.assert_called_with(
            "POST",
            "ml@domain.com/members.json",
            data={"members": '["member1@gmail.com"]', "upsert": "yes"},
        )
        self.assertEqual(responses, [request.return_value])

    @patch.object(MailingList, "request")
    def test_update_multiple_list_members_several_batches(self, request):
        responses = self.mailing_list.update_multiple_list_members(
            "ml@domain.com",
            ["member@gmail.com"] * (self.mailing_list.MEMBERS_UPLOAD_LIMIT + 1),
            True,
        )

        request.assert_has_calls(
            [
                call(
                    "POST",
                    "ml@domain.com/members.json",
                    data={
                        "members": json.dumps(
                            ["member@gmail.com"] * self.mailing_list.MEMBERS_UPLOAD_LIMIT
                        ),
                        "upsert": "yes",
                    },
                ),
                call(
                    "POST",
                    "ml@domain.com/members.json",
                    data={"members": json.dumps(["member@gmail.com"]), "upsert": "yes"},
                ),
            ]
        )
        self.assertEqual(responses, [request.return_value, request.return_value])

    @patch.object(MailingList, "request")
    def test_remove_list_member(self, request):
        response = self.mailing_list.remove_list_member(
            "ml@domain.com", "member@gmail.com"
        )

        request.assert_called_with("DELETE", "ml@domain.com/members/member@gmail.com")
        self.assertEqual(response, request.return_value)
