#!/usr/bin/env python

"""Logs module for SimpleMDMpy"""
#pylint: disable=invalid-name

import SimpleMDMpy.SimpleMDM

class Logs(SimpleMDMpy.SimpleMDM.Resource):
    """GET all the LOGS"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.url = self.api_url("/logs")
    
    def get_logs(self, starting_after=None, limit=None):
        """Returns logs, and I mean all the LOGS
        
        Args:
            starting_after (str, optional):  set to the id of the log object you
                want to start with. Defaults to the first object.
            limit (str, optional): A limit on the number of objects that will be
                returned per API call. Setting this will still return all logs.
                Defaults to 100.
        
        Returns:
            array: An array of dictionary log objects.
        """
        url = self.url
        params = {}
        if starting_after:
            params['starting_after'] = starting_after
        if limit:
            params['limit'] = limit
        return self.get_data(url, params=params)
