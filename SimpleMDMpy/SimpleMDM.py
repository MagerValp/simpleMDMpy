#!/usr/bin/env python

"""base module for calling simplemdm api"""
#pylint: disable=invalid-name

from builtins import str
from builtins import range
from builtins import object
import requests

class ApiError(Exception):
    """Catch for API Error"""
    pass

class Connection(object): #pylint: disable=old-style-class,too-few-public-methods
    """create connection with api key"""
    proxyDict = dict()

    def __init__(self, api_key):
        self.api_key = api_key

    def _url(self, path): #pylint: disable=no-self-use
        """base api url"""
        return 'https://a.simplemdm.com/api/v1' + path

    def _get_data(self, url, params=None):
        """GET call to SimpleMDM API"""
        start_id = 0
        has_more = True
        list_data = []
        if params is None:
            params = {}
        params["limit"] = 100
        while has_more:
            params["starting_after"] = start_id
            resp = requests.get(url, params, auth=(self.api_key, ""), proxies=self.proxyDict)
            if not 200 <= resp.status_code <= 207:
                raise ApiError(f"API returned status code {resp.status_code}")
            resp_json = resp.json()
            data = resp_json['data']
            # If the response isn't a list, return the single item.
            if not isinstance(data, list):
                return data
            # If it's a list we save it and see if there is more data coming.
            list_data.extend(data)
            has_more = resp_json.get('has_more', False)
            if has_more:
                start_id = data[-1].get('id')
        return list_data

    def _get_xml(self, url, params=None):
        """GET call to SimpleMDM API"""
        resp = requests.get(url, params, auth=(self.api_key, ""), proxies=self.proxyDict)
        return resp.content

    def _patch_data(self, url, data, files=None):
        """PATCH call to SimpleMDM API"""
        resp = requests.patch(url, data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _post_data(self, url, data, files=None):
        """POST call to SimpleMDM API"""
        resp = requests.post(url, data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _put_data(self, url, data, files=None):
        """PUT call to SimpleMDM API"""
        resp = requests.put(url, data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _delete_data(self, url):
        """DELETE call to SimpleMDM API"""
        return requests.delete(url, auth=(self.api_key, ""), proxies=self.proxyDict)
