"""SimpleMDMpy - A python API for interacting with the SimpleMDM API.
Official API documentation is available at https://api.simplemdm.com

A SimpleMDM API key is required."""

#pylint: disable=invalid-name


# Import exceptions
from SimpleMDMpy.Exceptions import *


# Imports for legacy API use
from SimpleMDMpy.Account import Account
from SimpleMDMpy.AppGroups import AppGroups
from SimpleMDMpy.Apps import Apps
from SimpleMDMpy.AssignmentGroups import AssignmentGroups
from SimpleMDMpy.CustomAttributes import CustomAttributes
from SimpleMDMpy.CustomConfigurationProfiles import CustomConfigurationProfiles
from SimpleMDMpy.DepServers import DepServers
from SimpleMDMpy.DeviceGroups import DeviceGroups
from SimpleMDMpy.Devices import Devices
from SimpleMDMpy.Enrollments import Enrollments
from SimpleMDMpy.InstalledApps import InstalledApps
from SimpleMDMpy.Logs import Logs
from SimpleMDMpy.LostMode import LostMode
from SimpleMDMpy.ManagedAppConfigs import ManagedAppConfigs
from SimpleMDMpy.PushCertificate import PushCertificate
from SimpleMDMpy.ScriptJobs import ScriptJobs
from SimpleMDMpy.Scripts import Scripts


# New session based API
from SimpleMDMpy.SimpleMDMSession import Session
