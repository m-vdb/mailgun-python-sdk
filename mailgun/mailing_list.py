"""Mailing list API."""
import json

from .base import ApiResource, silence_error


class MailingList(ApiResource):
    """
    Mailing list resource.
    """
    api_endpoint = 'lists'

    def create(self, address, name=None, description=None, access_level=None):
        """
        Create a mailing list.

        :param address:            required address of mailing list
        :param name:               optional name
        :param description:        optional description
        :param access_level:       optional access level: readonly (default), members, everyone
        """
        return self.request('POST', data={
            'address': address,
            'name': name,
            'description': description,
            'access_level': access_level,
        })

    def list(self):
        """
        List the existing mailing lists.
        """
        return self.request('GET')

    def delete(self, address):
        """
        Delete an existing mailing list.
        """
        return self.request('DELETE', address)

    @silence_error(400, 'Address already exists')
    def add_list_member(self, address, member_address, parameters=None, name=None):
        """
        Add a member to a mailing list.

        :param address:            address of mailing list
        :param member_address:     member email address
        :param parameters:         optional parameters, will be saved in the member `vars`
        :param name:               optional member name
        """
        endpoint = '{}/members'.format(address)
        return self.request('POST', endpoint, data={
            'subscribed': True,
            'address': member_address,
            'name': name,
            'vars': json.dumps(parameters),
        })

    def update_list_member(  # pylint: disable=too-many-arguments
            self, address, member_address, parameters=None, name=None, subscribed=None):
        """
        Update a member of a mailing list.

        :param address:            address of mailing list
        :param member_address:     member email address
        :param parameters:         optional parameters, will be saved in the member `vars`
        :param name:               optional member name
        :param subscribed:         optional, set to True to subscribe, False to unsubscribe
        """
        endpoint = '{}/members/{}'.format(address, member_address)
        return self.request('PUT', endpoint, data={
            'subscribed': subscribed,
            'name': name,
            'vars': json.dumps(parameters),
        })

    def update_multiple_list_members(self, address, members, upsert=False):
        """
        Update multiple members of a mailing list.

        :param address:            address of mailing list
        :param members:            members parameters to update
        :param upsert:             update existing members if True, else discards
        """
        endpoint = '{}/members.json'.format(address)
        return self.request('POST', endpoint, data={
            'members': json.dumps(members),
            'upsert': 'yes' if upsert else 'no',
        })

    @silence_error(404, r'Member .+ not found')
    def remove_list_member(self, address, member_address):
        """
        Remove a member from a mailing list.

        :param address:            address of mailing list
        :param member_address:     member email address
        """
        endpoint = '{}/members/{}'.format(address, member_address)
        return self.request('DELETE', endpoint)
