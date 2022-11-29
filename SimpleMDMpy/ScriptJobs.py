"""Scripts module for SimpleMDMpy"""


from SimpleMDMpy.SimpleMDM import Resource, ApiError


class ScriptJobs(Resource):
    """scripts module for SimpleMDMpy"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.url = self.api_url("/script_jobs")

    def get_job(self, job_id="all"):
        """Jobs represent scripts that have been set to run on a collection of
        devices. Jobs remain listed for one month.
        
        Args:
            job_id (int, optional): Returns a dictionary of the specified job
                id. By default, it returns a list of all jobs.
        
        Returns:
            dict: A single dictionary object with job information.
            array: An array of dictionary objects with job information.
        """
        url = self.url
        if job_id != 'all':
            url = url + "/" + str(job_id)
        return self.get_data(url)

    def create_job(self, script_id, device_ids=None, group_ids=None, assignment_group_ids=None):
        """
        You can use this method to upload a new script to your account.
        
        Args:
            script_id (int): Required. The ID of the script to be run on the devices
            device_ids (list of ints, optional): A list of device IDs to run
                the script on
            group_ids (list of ints, optional): A list of group IDs to run the
                script on. All macOS devices from these groups will be included.
            assignment_group_ids (list of ints, optional): A comma separated
                list of assignment group IDs to run the script on. All macOS
                devices from these assignment groups will be included.            
        
        Returns:
            dict: A dictionary object with job information.
        """
        params = {}
        if device_ids is not None:
            params['device_ids'] = ",".join(str(x) for x in device_ids)
        if group_ids is not None:
            params['group_ids'] = ",".join(str(x) for x in group_ids)
        if assignment_group_ids is not None:
            params['assignment_group_ids'] = ",".join(str(x) for x in assignment_group_ids)
        if not params:
            raise ApiError(f"At least one of device_ids, group_ids, or assignment_group_ids must be provided")
        params['script_id'] = str(script_id)
        resp = self.post_data(self.url, params)
        if not 200 <= resp.status_code <= 207:
            raise ApiError(f"Job creation failed with status code {resp.status_code}: {resp.content}")
        return resp.json()['data']

    def cancel_job(self, job_id):
        """
        You can use this method delete cancel a job. Jobs can only be canceled
        before the device has received the command.
        """
        url = self.url + "/" + str(job_id)
        return self.delete_data(url)
