"""Scripts module for SimpleMDMpy"""


from SimpleMDMpy.SimpleMDM import Resource, ApiError
from SimpleMDMpy.utils import legacy


class Scripts(Resource):
    """scripts module for SimpleMDMpy"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.url = self.api_url("/scripts")

    @legacy("get")
    def get_script(self, script_id="all"):
        """
        Returns a listing of all scripts in the account, or the script
        specified by id.
        
        Args:
            script_id (int, optional):  Returns a dictionary of the specified
                script id. By default, it returns a list of all scripts.
        
        Returns:
            dict: A single dictionary object with script information.
            array: An array of dictionary objects with script information.
        """
        return self.get(script_id)

    def get(self, script_id="all"):
        """
        Returns a listing of all scripts in the account, or the script
        specified by id.
        
        Args:
            script_id (int, optional):  Returns a dictionary of the specified
                script id. By default, it returns a list of all scripts.
        
        Returns:
            dict: A single dictionary object with script information.
            array: An array of dictionary objects with script information.
        """
        url = self.url
        if script_id != 'all':
            url = url + "/" + str(script_id)
        return self.get_data(url)

    @legacy("create")
    def create_script(self, name, variable_support, content):
        """
        You can use this method to upload a new script to your account.

        Args:
            name (str): The name for the script. This is how it will appear
                in the Admin UI.
            variable_support (bool): Whether or not to enable variable support
                in this script.
            content (str): The script content. All scripts must begin with a
                valid shebang such as #!/bin/sh to be processed.
        """
        return self.create(name, variable_support, content)

    def create(self, name, variable_support, content):
        """
        You can use this method to upload a new script to your account.

        Args:
            name (str): The name for the script. This is how it will appear
                in the Admin UI.
            variable_support (bool): Whether or not to enable variable support
                in this script.
            content (str): The script content. All scripts must begin with a
                valid shebang such as #!/bin/sh to be processed.
        """
        params = {
            'name': name,
            'variable_support': "1" if variable_support else "0",
        }
        files = {
            'file': ('script.sh', content)
        }
        resp = self.post_data(self.url, params, files)
        if not 200 <= resp.status_code <= 207:
            raise ApiError(f"Script creation failed with status code {resp.status_code}: {resp.content}")
        return resp.json()['data']

    @legacy("update")
    def update_script(self, script_id, name=None, variable_support=None, content=None):
        """
        You can use this method to update an existing script in your account.
        Any existing Script Jobs will not be changed.
        """
        return self.update(script_id, name, variable_support, content)

    def update(self, script_id, name=None, variable_support=None, content=None):
        """
        You can use this method to update an existing script in your account.
        Any existing Script Jobs will not be changed.
        """
        url = self.url + "/" + str(script_id)
        params = {}
        files = None
        if name is not None:
            params['name'] = name
        if variable_support is not None:
            params['variable_support'] = "1" if variable_support else "0"
        if content is not None:
            files = {
                'file': ('script.sh', content)
            }
        if not params and not files:
            raise ApiError(f"Missing updated variables.")
        resp = self.patch_data(url, params, files)
        if not 200 <= resp.status_code <= 207:
            raise ApiError(f"Script update failed with status code {resp.status_code}: {resp.content}")
        return resp.json()['data']

    @legacy("delete")
    def delete_script(self, script_id):
        """You can use this method to delete a script from your account. Any
        existing Script Jobs will not be changed."""
        return self.delete(script_id)

    def delete(self, script_id):
        """You can use this method to delete a script from your account. Any
        existing Script Jobs will not be changed."""
        url = self.url + "/" + str(script_id)
        return self.delete_data(url)
