# SAKÉ: Simple ASCII Kodi Emulator
[![License](https://img.shields.io/github/license/retrospect-addon/kodi.emulator.ascii?color=brightgreen)](LICENSE.md)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/retrospect-addon/kodi.emulator.ascii/unit-tests/master)](https://github.com/retrospect-addon/kodi.emulator.ascii/actions?query=workflow%3Aunit-tests)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=retrospect-addon%3Akodi.emulator.ascii&metric=alert_status)](https://sonarcloud.io/dashboard?id=retrospect-addon%3Akodi.emulator.ascii)
[![Python](https://img.shields.io/badge/python-2.7%20%7C%203.6-blue?logo=python)](https://kodi.tv/article/attention-addon-developers-migration-python-3)

![alt text](https://github.com/retrospect-addon/kodi.emulator.ascii/raw/master/sake.png "Simple ASCII Kodi Emulator")

## _SAKÉ_: your favourite 'drink' for debugging and developing Kodi Python add-ons
SAKÉ can help you to debug and develop Kodi Python add-ons. It contains a set of libraries that try to mimic the functionality of the corresponding Kodi modules:

| Module       | Purpose                                |
|--------------|----------------------------------------|
| `xbmc`       | General functions on Kodi              |
| `xbmcaddon`  | Kodi’s addon class                     |
| `xbmcgui`    | GUI functions on Kodi.                 |
| `xbmcplugin` | Plugin functions on Kodi.              |
| `xbmcvfs`    | Virtual file system functions on Kodi. |

Not all libraries are present and certainly not all methods are implemented. Currently missing are:

| Module    | Purpose           |
|-----------|-------------------|
| `xbmcdrm` | Kodi’s DRM class. |

Feel free to contribute to the completion using Pull Requests for this repository.

### Using _SAKÉ_
SAKÉ can be installed using the `pip install` command:

    $ pip install sakee
    
This will install SAKÉ in the active Python installation. It will be available directly to all your Python scripts. If you choose to not use `pip install` and want to run it from a specific (custom) location then you will need to include its path the Python paths. Either via:

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
| `KODI_ACTIVE_PROFILE` | _SAKÉ_ will assume that you don't have any Kodi profiles, but in case you have, you can specify what profile to use for the add-on settings. |
| `KODI_INTERACTIVE`   | Normally, _SAKÉ_ will try to interact with you: Whenever there should be a dialog shown within Kodi, _SAKÉ_ will present you with an ASCII version and wait for a response. You can disable this by setting this environment variable to "0". _SAKÉ_ will not disturb you and will continue. However, _SAKÉ_ will answer those dialogs for you and that **might result in unwanted actions**, but it might come in handy while running unit tests.|
| `KODI_STUB_VERBOSE` | If set to "1" will make _SAKÉ_ a bit more verbose. |
| `KODI_STUB_RPC_RESPONSES` | Specifies the folder from which to read JSON RPC responses. If you don't set this, you won't be able to use `xbmc.executeJSONRPC` |
| `KODI_STUB_INPUT` | Specify the default input for the keyboard input |

### JSON RPC responses
In order to respond to the JSON RPC requests, issued via `executeJSONRPC`, a folder with response files can be configured using the `KODI_STUB_RPC_RESPONSES` environment variable (see above). This folder should contain response files with the following naming conversions:

    <method_name>.json
    
So, for instance `favourites.getfavourites.json`. Inside the file there is: 

- A single complete JSON response. In this case, the complete content of the file will be used, as is, as the JSON RPC response.
- A list of JSON request-response pairs with different input parameters. Using the input parameters of the JSON RPC request, the correct response is determined and returned as the JSON RPC response.

In the latter case, the content of a stub file could look like this:

```json
[
  {
    "request": {
      "params": {
        "setting": "network.usehttpproxy"
      },
      "jsonrpc": "2.0",
      "method": "Settings.GetSettingValue",
      "id": 0
    },
    "response": {
      "id": 5,
      "jsonrpc": "2.0",
      "result": {
        "value": false
      }
    }
  },
  {
    "request": {
      "params": {
        "setting": "network.httpproxyusername"
      },
      "jsonrpc": "2.0",
      "method": "Settings.GetSettingValue",
      "id": 0
    },
    "response": {
      "id": 5,
      "jsonrpc": "2.0",
      "result": {
        "value": true
      }
    }
  }
]
```

This stub file contains responses for the method `Settings.GetSettingValue` for the setting `network.usehttpproxy` and `network.httpproxyusername`.

If no file with matching method name is found or the file does not contain the correct responses an 'OK' is returned:

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "OK"
}
``` 

Just like most of the Kodi JSON RPC calls do.
