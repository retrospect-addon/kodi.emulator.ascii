# SPDX-License-Identifier: GPL-3.0
import os
import re
import subprocess

from sakee import addoninfo


class BuiltinApi(object):
    __ADDON_INFO = None

    def __init__(self):
        """ Initialise the Built-in API Implementation. """
        if BuiltinApi.__ADDON_INFO is None:
            BuiltinApi.__ADDON_INFO = addoninfo.get_add_on_info_from_calling_script()

        self.function_mapping = {
            'RunPlugin': self.RunPlugin,
        }

    def handle(self, function):
        """ Handle the Built-in function.

        :param obj function:        The built-in function call.

        """
        method, params = re.search(r'^([^\(\s]*)(?:\((.*?)\))?', function).groups()
        try:
            # Replace . with _ since we have function-names with dots in it.
            method_reference = getattr(self, method.replace('.', '_'))
        except AttributeError:
            raise NotImplementedError

        method_reference(*params.split(','))

    @staticmethod
    def RunPlugin(plugin):
        """ Runs the plugin. Full path must be specified. Does not work for folder plugins.

        :param str plugin:          plugin:// URL to script.

        """
        addon, path, params = re.search(r'^plugin://([^?\s/]*)([^?\s]*)(\?.*)?', plugin).groups()

        try:
            addon_info = addoninfo.read_addon_xml(os.path.join(BuiltinApi.__ADDON_INFO.kodi_home_path, 'addons', addon, 'addon.xml'))
        except FileNotFoundError:
            raise ValueError('Addon %s not found' % addon)

        addon_entry = os.path.join(BuiltinApi.__ADDON_INFO.kodi_home_path, 'addons', addon, addon_info.get('pluginsource'))
        addon_route = 'plugin://' + addon + path
        addon_params = params or ''

        # This causes argv[0] to be addon_entry, while it's skipped in a real Kodi.
        subprocess.Popen(['python', addon_entry, addon_route, '-1', addon_params, 'resume:false'])
