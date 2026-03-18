#!/usr/bin/env python

"""base module for calling simplemdm api"""
#pylint: disable=invalid-name

from builtins import str
from builtins import range
from builtins import object
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time


class ApiError(Exception):
    """Catch for API Error"""
    pass

class Connection(object): #pylint: disable=old-style-class,too-few-public-methods
    """create connection with api key"""
    proxyDict = dict()

    last_device_req_timestamp = 0
    device_req_rate_limit = 1.0

    def __init__(self, api_key):
        self.api_key = api_key
        # setup a session that can retry, helps with rate limiting end-points
        # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
        # https://macadmins.slack.com/archives/C4HJ6U742/p1652996411750219
        retry_strategy = Retry(
            total = 5,
            backoff_factor = 1,
            status_forcelist = [500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def __del__(self):
        # this runs when the Connection object is being deinitialized
        # this properly closes the session
        self.session.close()

    def _url(self, path): #pylint: disable=no-self-use
        """base api url"""
        return 'https://a.simplemdm.com/api/v1' + path

    # TODO: make _is_devices_req generic for any future rate limited endpoints
    def _is_devices_req(self, url):
        return url.startswith(self._url("/devices"))

    def _get_data(self, url, params=None):
        """GET call to SimpleMDM API"""
        has_more = True
        list_data = []
        # by using the local req_params variable, we can set our own defaults if
        # the parameters aren't included with the input params. This is needed
        # so that certain other functions, like Logs.get_logs(), can send custom
        # starting_after and limit parameters.
        if params is None:
            req_params = {}
        else:
            req_params = params.copy()
        req_params['limit'] = req_params.get('limit', 100)
        while has_more:
            # Calls to /devices should be rate limited
            if self._is_devices_req(url):
                seconds_since_last_device_req = time.monotonic() - self.last_device_req_timestamp
                if seconds_since_last_device_req < self.device_req_rate_limit:
                    time.sleep(self.device_req_rate_limit - seconds_since_last_device_req)
            self.last_device_req_timestamp = time.monotonic()
            while True:
                resp = self.session.get(url, params=req_params, auth=(self.api_key, ""), proxies=self.proxyDict)
                # A 429 means we've hit the rate limit, so back off and retry
                if resp.status_code == 429:
                    time.sleep(1)
                else:
                    break
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
                req_params["starting_after"] = data[-1].get('id')
        return list_data

    def _get_xml(self, url, params=None):
        """GET call to SimpleMDM API"""
        resp = requests.get(url, params, auth=(self.api_key, ""), proxies=self.proxyDict)
        return resp.content

    def _patch_data(self, url, data, files=None):
        """PATCH call to SimpleMDM API"""
        resp = requests.patch(url, json=data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _post_data(self, url, data, files=None):
        """POST call to SimpleMDM API"""
        resp = requests.post(url, json=data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _put_data(self, url, data, files=None):
        """PUT call to SimpleMDM API"""
        resp = requests.put(url, json=data, auth=(self.api_key, ""), \
            files=files, proxies=self.proxyDict)
        return resp

    def _delete_data(self, url):
        """DELETE call to SimpleMDM API"""
        return requests.delete(url, auth=(self.api_key, ""), proxies=self.proxyDict)
