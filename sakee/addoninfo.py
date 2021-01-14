# SPDX-License-Identifier: GPL-3.0

import os
import xml.etree.ElementTree as ET
from collections import namedtuple

from sakee.colors import Colors
from sakee.stub import KodiStub

# Custom AddonData type
AddonData = namedtuple('AddonData', [
    'kodi_home_path',  # data path (either portable of user path)
    'add_on_id',  # the add-on id
    'add_on_path',  # the full path to the add-on
    'kodi_profile_path'  # the full path to the add-on profile folder
])

__add_on_infos = {}


def get_add_on_info_from_calling_script(add_on_id=None, print_info=False):
    if add_on_id is not None:
        # Always print details for specific add-ons
        print_info = True

    add_on_info = __add_on_infos.get(add_on_id)
    if add_on_info:
        return add_on_info

    # What is the Kodi Home path?
    assert os.path.isfile("addon.xml"), "Working directory outside add-on path: {}".format(os.getcwd())
    calling_add_on_path = os.getcwd()

    # Get the generic Kodi paths
    kodi_home_path = os.environ.get("KODI_HOME")
    if kodi_home_path:
        # We only need the ID from the path.
        _, path_add_on_id = calling_add_on_path.rsplit(os.sep, 1)
    else:
        # determine it based on the running path
        kodi_home_path, addon_name, path_add_on_id = os.getcwd().rsplit(os.sep, 2)

    kodi_home_path = os.path.abspath(kodi_home_path)
    assert os.path.isdir(kodi_home_path), \
        "Kodi home path (special://home) does not exist: '{}'".format(kodi_home_path)

    # Find the very first script called to determine the add-on ID if it was not specified
    add_on_id = add_on_id or path_add_on_id

    # Active add-on path
    if add_on_id is None or add_on_id == path_add_on_id:
        # We should use the data from the current calling add-on
        add_on_path = calling_add_on_path
    else:
        # We should set it to the requested add-on based on the given add-on ID
        add_on_path = os.path.join(kodi_home_path, "addons", add_on_id)
        if not os.path.isdir(add_on_path) and "portable_data" in calling_add_on_path:
            add_on_path = os.path.abspath(os.path.join(kodi_home_path, "..", "addons", add_on_id))
    assert os.path.isdir(add_on_path), \
        "Invalid add-on dir for add-on '{}': {}".format(add_on_id, add_on_path)

    # The active profile path
    if "KODI_PROFILE" in os.environ:
        add_on_profile_path = os.path.abspath(os.environ["KODI_PROFILE"])
    else:
        add_on_profile_path = os.path.join(kodi_home_path, "userdata")

    add_on_profile_path = os.path.abspath(add_on_profile_path)
    assert os.path.isdir(add_on_profile_path), \
        "Invalid Kodi master profile dir (special://masterprofile): {}".format(add_on_profile_path)

    if "KODI_ACTIVE_PROFILE" in os.environ:
        add_on_profile_path = os.path.join(
            add_on_profile_path, "profiles", os.environ["KODI_ACTIVE_PROFILE"])

        assert os.path.isdir(add_on_profile_path), \
            "Invalid Kodi profile dir (special://profile): {}".format(add_on_profile_path)

    a = AddonData(
        kodi_home_path=kodi_home_path,
        add_on_id=add_on_id,
        add_on_path=add_on_path,
        kodi_profile_path=add_on_profile_path
    )

    __add_on_infos[add_on_id] = a
    if add_on_id == path_add_on_id:
        __add_on_infos[None] = a

    if not print_info:
        return a

    KodiStub.print_line(
        "Found Add-on info: \n"
        "- Kodi Home (special://home):       {} \n"
        "- Add-on ID:                        {} \n"
        "- Add-on Path:                      {} \n"
        "- Kodi Profile (special://profile): {} \n"
            .format(a.kodi_home_path, a.add_on_id, a.add_on_path, a.kodi_profile_path),
        color=Colors.Blue
    )
    return a


def read_addon_xml(path):
    """Parse the addon.xml and return an info dictionary"""
    info = dict(
        path='./',
        profile='special://userdata',
        type='xbmc.python.pluginsource',
    )

    tree = ET.parse(path)
    root = tree.getroot()

    info.update(root.attrib)  # Add 'id', 'name' and 'version'
    info['author'] = info.pop('provider-name')

    for child in root:
        if child.attrib.get('point') == 'xbmc.python.pluginsource':
            info['pluginsource'] = child.attrib.get('library')
            continue

        if child.attrib.get('point') == 'xbmc.addon.metadata':
            for grandchild in child:
                # Handle assets differently
                if grandchild.tag == 'assets':
                    for asset in grandchild:
                        info[asset.tag] = asset.text
                    continue
                # Not in English ?  Drop it
                if grandchild.attrib.get('lang', 'en_GB') != 'en_GB':
                    continue
                # Add metadata
                info[grandchild.tag] = grandchild.text
            continue

    return info
