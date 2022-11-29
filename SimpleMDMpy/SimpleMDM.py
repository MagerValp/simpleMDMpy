"""Resource classes to handle requests to the API endpoints"""


#pylint: disable=invalid-name

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
from SimpleMDMpy.Exceptions import *


class Resource: #pylint: disable=old-style-class,too-few-public-methods
    """Create connection with API key"""

    def __init__(self, api_key, proxies=None, timeout=30, retry_count=2):
        self.request_config = {
            "auth": (api_key, ""),
            "proxies": proxies if proxies is not None else {},
            "timeout": timeout,
        }

        # Setup a session that can retry, helps with rate limiting end-points
        # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#retry-on-failure
        # https://macadmins.slack.com/archives/C4HJ6U742/p1652996411750219
        retry_strategy = Retry(
            total = retry_count,
            backoff_factor = 1,
            status_forcelist = [500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def __del__(self):
        # This runs when the Resource object is being deinitialized
        # This properly closes the session
        self.session.close()

    def api_url(self, path): #pylint: disable=no-self-use
        """Base API URL"""
        return 'https://a.simplemdm.com/api/v1' + path

    def pre_request_hook(self):
        """Called before a request call is made to allow for customization"""
        pass

    def _get_response_errors(self, resp):
        try:
            errors = resp.json()["errors"]
            return ", ".join(x["title"] for x in errors)
        except:
            return resp.content.decode("utf-8", errors="backslashreplace")

    def _requests_call(self, method, url, **kwargs):
        """Perform call using specified method and optional args"""
        args = {**kwargs, **self.request_config}
        try:
            while True:
                self.pre_request_hook()
                resp = self.session.request(method, url, **args)
                # A 429 means we've hit the rate limit, so back off and retry
                if method == "get" and resp.status_code == 429:
                    time.sleep(1)
                else:
                    break
        except requests.exceptions.RequestException as e:
            raise ApiError(f"API request failed: {e}")
        if 200 <= resp.status_code <= 207 or resp.status_code == 429:
            return resp
        error_msg = f"API returned status code {resp.status_code}"
        try:
            server_error_msg = self._get_response_errors(resp)
            error_msg += f": {server_error_msg}"
        except:
            pass
        raise ApiError(error_msg)

    def get_data(self, url, params=None):
        """GET call to SimpleMDM API. Handles json decoding and pagination."""
        has_more = True
        list_data = []
        # By using the local req_params variable, we can set our own defaults if
        # the parameters aren't included with the input params. This is needed
        # so that certain other functions, like Logs.get_logs(), can send custom
        # starting_after and limit parameters.
        if params is None:
            req_params = {}
        else:
            req_params = params.copy()
        req_params['limit'] = req_params.get('limit', 100)
        while has_more:
            resp = self._requests_call("get", url, params=req_params)
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

    def get_raw_content(self, url, params=None):
        """GET call to SimpleMDM API. Returns the raw response content."""
        resp = self._requests_call("get", url, params=params)
        return resp.content


    def patch_data(self, url, data, files=None):
        """PATCH call to SimpleMDM API"""
        resp = self._requests_call("patch", url, data=data, files=files)
        return resp

    def post_data(self, url, data, files=None):
        """POST call to SimpleMDM API"""
        resp = self._requests_call("post", url, data=data, files=files)
        return resp

    def put_data(self, url, data, files=None):
        """PUT call to SimpleMDM API"""
        resp = self._requests_call("put", url, data=data, files=files)
        return resp

    def delete_data(self, url):
        """DELETE call to SimpleMDM API"""
        resp = self._requests_call("delete", url)
        return resp


class RateLimitedResource(Resource):
    """Create rate limited connection with API key"""

    def __init__(self, *args, **kwargs):
        self.last_req_timestamp = 0.0
        self.min_req_interval = 1.0
        super().__init__(*args, **kwargs)

    def pre_request_hook(self):
        """Implement rate limiting to this request endpoint"""
        seconds_since_last_req = time.monotonic() - self.last_req_timestamp
        if seconds_since_last_req < self.min_req_interval:
            time.sleep(self.min_req_interval - seconds_since_last_req)
        self.last_req_timestamp = time.monotonic()

