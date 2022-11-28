#!/usr/bin/env python

"""devices module for SimpleMDMpy"""
#pylint: disable=invalid-name

import SimpleMDMpy.SimpleMDM

class Devices(SimpleMDMpy.SimpleMDM.Connection):
    """devices module for SimpleMDMpy"""
    def __init__(self, api_key):
        super().__init__(self, api_key)
        self.url = self._url("/devices")

    def get_device(self, device_id="all", search=None, include_awaiting_enrollment=False):
        """
        Returns a device specified by id. If no ID or search is specified all
        devices will be returned.
        
        Args:
            device_id (str, optional):  Returns a dictionary of the specified
                device id. By default, it returns a list of all devices. If a
                device_id and search is specified, then search will be ignored.
            search (str, optional): Returns a list of devices that match the
                search criteria. Defaults to None. Ignored if device_id is set.
            include_awaiting_enrollment (bool, optional): Returns a list of all
                devices including devices in the "awaiting_enrollment" state.
        
        Returns:
            dict: A single dictionary object with device information.
            array: An array of dictionary objects with device information.
        """
        url = self.url
        params = {'include_awaiting_enrollment': include_awaiting_enrollment}
        # if a device ID is specified, then ignore any searches
        if device_id != 'all':
            url = url + "/" + str(device_id)
        elif search:
            params['search'] = search
        return self._get_data(url, params)

    def create_device(self, name, group_id):
        """Creates a new device object in SimpleMDM. The response
        body includes an enrollment URL that can be used once to
        enroll a physical device."""
        data = {'name': name, 'group_id': group_id}
        return self._post_data(self.url, data)

    def update_device(self, device_id, name=None, device_name=None):
        """Update the SimpleMDM name and/or device name of a device object."""
        url = self.url + "/" + str(device_id)
        data = {}
        if name is not None:
            data.update({'name':name})
        if device_name is not None:
            data.update({'device_name':device_name})
        if data == {}:
            raise Exception(f"Missing name and/or device_name variables.")
        return self._patch_data(url, data)

    def delete_device(self, device_id):
        """Unenroll a device and remove it from the account."""
        url = self.url + "/" + str(device_id)
        return self._delete_data(url) #pylint: disable=too-many-function-args

    def list_profiles(self, device_id):
        """Returns a listing of profiles that are directly assigned to the device."""
        url = self.url + "/" + str(device_id) + "/profiles"
        return self._get_data(url)

    def list_installed_apps(self, device_id):
        """Returns a listing of the apps installed on a device."""
        url = self.url + "/" + str(device_id) + "/installed_apps"
        return self._get_data(url)

    def list_users(self, device_id):
        """Returns a listing of the user accounts on a device."""
        url = self.url + "/" + str(device_id) + "/users"
        return self._get_data(url)

    def push_apps_device(self, device_id):
        """You can use this method to push all assigned apps
        to a device that are not already installed."""
        url = self.url + "/" + str(device_id) + "/push_apps"
        data = {}
        return self._post_data(url, data)

    def restart_device(self, device_id):
        """This command sends a restart command to the device."""
        url = self.url + "/" + str(device_id) + "/restart"
        data = {}
        return self._post_data(url, data)

    def shutdown_device(self, device_id):
        """This command sends a shutdown command to the device."""
        url = self.url + "/" + str(device_id) + "/shutdown"
        data = {}
        return self._post_data(url, data)

    def lock_device(self, device_id, message, phone_number, pin=None):
        """You can use this method to lock a device and optionally display
        a message and phone number. The device can be unlocked with the
        existing passcode of the device."""
        url = self.url + "/" + str(device_id) + "/lock"
        data = {'message': message, 'phone_number': phone_number, 'pin':pin}
        return self._post_data(url, data)

    def clear_passcode_device(self, device_id):
        """You can use this method to unlock and remove the passcode of a device."""
        url = self.url + "/" + str(device_id) + "/clear_passcode"
        data = {}
        return self._post_data(url, data)

    def clear_firmware_password(self, device_id):
        """You can use this method to remove the firmware password from a device.
        The firmware password must have been originally set using SimpleMDM for
        this to complete successfully."""
        url = self.url + "/" + str(device_id) + "/clear_firmware_password"
        data = {}
        return self._post_data(url, data)

    def wipe_device(self, device_id):
        """You can use this method to erase all content and settings stored on a
        device. The device will be unenrolled from SimpleMDM and returned to a
        factory default configuration."""
        url = self.url + "/" + str(device_id) + "/wipe"
        data = {}
        return self._post_data(url, data)

    def update_os(self, device_id):
        """You can use this method to update a device to the latest OS version.
        Currently supported by iOS devices only."""
        url = self.url + "/" + str(device_id) + "/update_os"
        data = {}
        return self._post_data(url, data)

    def enable_remote_desktop(self, device_id):
        """You can use this method to enable remote desktop. Supported by macOS 10.14.4+ devices only."""
        url = self.url + "/" + str(device_id) + "/remote_desktop"
        data = {}
        return self._post_data(url, data)

    def disable_remote_desktop(self, device_id):
        """You can use this method to disable remote desktop. Supported by macOS 10.14.4+ devices only."""
        url = self.url + "/" + str(device_id) + "/remote_desktop"
        return self._delete_data(url)

    def refresh_device(self, device_id):
        """Request a refresh of the device information and app inventory.
        SimpleMDM will update the inventory information when the device responds
        to the request."""
        url = self.url + "/" + str(device_id) + "/refresh"
        data = {}
        return self._post_data(url, data)

    def get_custom_attributes(self, device_id):
        """Get all custom attributes for a device."""
        url = self.url + "/" + str(device_id) + "/custom_attribute_values"
        data = {}
        return self._get_data(url, data)

    def get_custom_attribute(self, device_id, custom_attribute_name):
        """Get a specific custom attribute for a device."""
        url = self.url + "/" + str(device_id) + "/custom_attribute_values/" + custom_attribute_name
        data = {}
        return self._get_data(url, data)

    def set_custom_attribute(self, value, device_id, custom_attribute_name):
        """Set a custom attribute value."""
        url = self.url + "/" + str(device_id) + "/custom_attribute_values/" + custom_attribute_name
        data = {'value': value}
        return self._put_data(url, data)
