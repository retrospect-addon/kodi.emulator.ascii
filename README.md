# SAKE: Simple ASCII Kodi Emulator
[![License](https://img.shields.io/github/license/retrospect-addon/kodi.emulator.ascii?color=brightgreen)](LICENSE.md)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=retrospect-addon%3Akodi.emulator.ascii&metric=alert_status)](https://sonarcloud.io/dashboard?id=retrospect-addon%3Akodi.emulator.ascii)
[![Python](https://img.shields.io/badge/python-2.7%20%7C%203.6-blue?logo=python)](https://kodi.tv/article/attention-addon-developers-migration-python-3)

![alt text](sake.png "Simple ASCII Kodi Emulator")

## _SAKE_: your favourite 'drink' for debugging and developiong Kodi Python add-ons
SAKE can help you to debug and develop Kodi Python add-ons. It contains a set of libraries that try to mimic the functionality of the corresponding Kodi modules:

| Module        | Purpose                   |
|---------------|---------------------------|
|`xbmc`         | General functions on Kodi |
|`xbmcaddon`    | Kodi’s addon class        |
|`xbmcgui`      | GUI functions on Kodi.    |
|`xbmcplugin`   | Plugin functions on Kodi. |


Not all libraries are present and certainly not all methods are implemented. Currently missing are:

| Module        | Purpose                   |
|---------------|---------------------------|
|`xbmcvfs`      | Virtual file system functions on Kodi.|
|`xbmcdrm`      | Kodi’s DRM class          |

Feel free to contribute to the completion using Pull Requests for this repository.

### Using _SAKE_
In order to use _SAKE_ for development Kodi add-ons, you will need to include it's path the the Python paths. Eiter via:

```Python
sys.path.append('<path to SAKE>')
```

Or by appending the _SAKE_ path to the Python path environment variable: `PYTHONPATH`
