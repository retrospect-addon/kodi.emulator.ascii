# SAKÉ: Simple ASCII Kodi Emulator
[![License](https://img.shields.io/github/license/retrospect-addon/kodi.emulator.ascii?color=brightgreen)](LICENSE.md)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=retrospect-addon%3Akodi.emulator.ascii&metric=alert_status)](https://sonarcloud.io/dashboard?id=retrospect-addon%3Akodi.emulator.ascii)
[![Python](https://img.shields.io/badge/python-2.7%20%7C%203.6-blue?logo=python)](https://kodi.tv/article/attention-addon-developers-migration-python-3)

![alt text](https://github.com/retrospect-addon/kodi.emulator.ascii/raw/master/sake.png "Simple ASCII Kodi Emulator")

## _SAKÉ_: your favourite 'drink' for debugging and developiong Kodi Python add-ons
SAKÉ can help you to debug and develop Kodi Python add-ons. It contains a set of libraries that try to mimic the functionality of the corresponding Kodi modules:

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

### Using _SAKÉ_
SAKÉ can be installed using the `pip install` command:

    $ pip install sakee
    
This will install SAKÉ in the active Python installation. It will be available directly to all your Python scripts. If you choose to not use `pip install` and want to run it from a specific (custom) location then you you will need to include its path the the Python paths. Eiter via:

```Python
sys.path.append('<path to SAKÉ>')
```

Or by appending the _SAKÉ_ path to the Python path environment variable: `PYTHONPATH`

### Configuration
_SAKÉ_ requires you to run with your add-on as the main _working directory_. Running it outside of that directory will fail. 

If your add-on is in a subfolder of Kodi's `addons` folder, you are done. _SAKÉ_ will try to find its own way and determine what your Kodi path is and where your profile is stored. However, if you are running it standalone, so without Kodi at all, or if _SAKÉ_ got 'drunk' and lost its way, you can always specify some directions using environment variables as follows:

| Environment Variable | Description |
|----------------------|-------------|
| `KODI_HOME`          | If specified, will force _SAKÉ_ to look at that path for Kodi's home path. |
| `KODI_PROFILE` | If specified, will force _SAKÉ_ to use this folder as the Kodi 'master' profile (user_data) folder. This will disable the auto detection of the profile folder based on Kodi's home path. |
| `KODI_ACTIVE_PROFILE` | _SAKÉ_ will asume that you don't have any Kodi profiles, but in case  you have, you can specify what profile to use for the add-on settings. |
| `KODI_INTERACTIVE`   | Normally, _SAKÉ_ will try to interact with you: Whenever there should be a dialog shown within Kodi, _SAKÉ_ will present you with an ASCII version and wait for a response. You can disable this by setting this environment variable to "0". _SAKÉ_ will not disturb you and will continue. However, _SAKÉ_ will answer those dialogs for you and that **might result in unwanted actions**, but it might come in handy while running unit tests.|
| `KODI_STUB_VERBOSE` | If set to "1" will make _SAKÉ_ a bit more verbose. |
| `KODI_STUB_RPC_RESPONSES` | Specifies the folder from which to read JSON RPC responses. If you don't set this, you won't be able to use `xbmc.executeJSONRPC` |
