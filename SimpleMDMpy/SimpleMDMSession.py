"""Session handling for SimpleMDM API"""


import os

from SimpleMDMpy import *


class Session:
    """A session object is the main way to use the SimpleMDMpy API.

    Instantiate it with an appropriate API key:
        
        import SimpleMDMpy
        session = SimpleMDMpy.Session(api_key="hbiBOR5NEhbw4u…")

    Or you can load the API key from an environement variable instead:

        session = SimpleMDMpy.Session(key_from_env="API_KEY")

    """

    def __init__(self, api_key=None, key_from_env=None, **conn_args):
        if api_key is None and key_from_env is not None:
            api_key = self._load_key_from_env(key_from_env)
        self.account = Account(api_key, **conn_args)
        self.appGroups = AppGroups(api_key, **conn_args)
        self.apps = Apps(api_key, **conn_args)
        self.assignmentGroups = AssignmentGroups(api_key, **conn_args)
        self.customAttributes = CustomAttributes(api_key, **conn_args)
        self.customConfigurationProfiles = CustomConfigurationProfiles(api_key, **conn_args)
        self.depServers = DepServers(api_key, **conn_args)
        self.deviceGroups = DeviceGroups(api_key, **conn_args)
        self.devices = Devices(api_key, **conn_args)
        self.enrollments = Enrollments(api_key, **conn_args)
        self.installedApps = InstalledApps(api_key, **conn_args)
        self.logs = Logs(api_key, **conn_args)
        self.lostMode = LostMode(api_key, **conn_args)
        self.managedAppConfigs = ManagedAppConfigs(api_key, **conn_args)
        self.pushCertificate = PushCertificate(api_key, **conn_args)
        self.scriptJobs = ScriptJobs(api_key, **conn_args)
        self.scripts = Scripts(api_key, **conn_args)

    def _load_key_from_env(self, name):
        api_key = os.getenv(name)
        if not api_key:
            raise ApiError(f"{name} environment variable not set")
        return api_key
