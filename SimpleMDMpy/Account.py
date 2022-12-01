#!/usr/bin/env python

"""accounts module for SimpleMDMpy"""
#pylint: disable=invalid-name

import SimpleMDMpy.SimpleMDM
from SimpleMDMpy.utils import legacy

class Account(SimpleMDMpy.SimpleMDM.Resource):
    """account class provides auth and basic account details"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.url = self.api_url("/account")

    @legacy("show")
    def get_account_details(self):
        """returns account details as dict"""
        return self.get_data(self.url)

    def show(self):
        """Retrieve information about your account. Subscription information is only available for accounts on a manual billing plan."""
        return self.get_data(self.url)

    @legacy("update")
    def set_account_details(self, name=None, country_code=None):
        """set account detail"""
        return self.update(name, country_code)

    def update(self, name=None, country_code=None):
        """set account detail"""
        data = {}
        if name:
            data['name'] = name
        if country_code:
            data['apple_store_country_code'] = country_code
        return self.patch_data(self.url, data)
