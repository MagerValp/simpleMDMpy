#!/usr/bin/env python

""" apps module for SimpleMDMpy"""
#pylint: disable=invalid-name

import SimpleMDMpy.SimpleMDM
from SimpleMDMpy.utils import legacy

class Apps(SimpleMDMpy.SimpleMDM.Resource):
    """ apps module for SimpleMDMpy"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.url = self.api_url("/apps")

    @legacy("get")
    def get_app(self, app_id="all"):
        """list app, if none specified all return"""
        return self.get(app_id)

    def get(self, app_id="all"):
        """Retrieve the specified app, or a list of all if no app_id is
        specified"""
        url = self.url
        if app_id != 'all':
            url = url + "/" + app_id
        return self.get_data(url)

    @legacy("create")
    def create_app(self, name=None, app_store_id=None, bundle_id=None, binary=None):
        """upload an app binary"""
        return self.create(name, app_store_id, bundle_id, binary)

    def create(self, name=None, app_store_id=None, bundle_id=None, binary=None):
        """You can use this method to add an App Store app, upload an enterprise iOS app, or upload macOS package to your app catalog.
        One and only one of of app_store_id, bundle_id, or binary must be specified. Name can optionally be specified if binary
        is specified."""
        data = {}
        files = {}
        if name:
            data['name'] = name
        if app_store_id:
            data['app_store_id'] = app_store_id
        elif bundle_id:
            data['bundle_id'] = bundle_id
        elif binary:
            files['binary'] = open(binary, 'rb')
        return self.post_data(self.url, data, files)

    @legacy("update")
    def update_app(self, app_id, binary=None, name=None):
        """update an apps info binary etc"""
        return self.update(app_id, binary, name)

    def update(self, app_id, binary=None, name=None):
        """You can use this method to update the binary of an existing app."""
        url = self.url + "/" + app_id
        data = {}
        files = {}
        if name:
            data['name'] = name
        if binary:
            files['binary'] = open(binary, 'rb')
        return self.patch_data(url, data, files)

    @legacy("delete")
    def delete_app(self, app_id):
        """delete an app"""
        return self.delete(app_id)

    def delete(self, app_id):
        url = self.url + "/" + app_id
        data = {}
        return self.delete_data(url, data) #pylint: disable=too-many-function-args
