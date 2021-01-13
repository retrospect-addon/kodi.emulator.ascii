# SPDX-License-Identifier: GPL-3.0

import os
import sys


def run(entrypoint, *args):
    """ Run the specified entrypoint in the background, and modify the args so it behaves like Kodi would run it. """

    # Run Add-on in another instance
    import subprocess
    subprocess.Popen(['python', __file__, entrypoint, *args])


if __name__ == "__main__":
    # Remove the first argument of sys.argv, that's this file
    sys.argv.pop(0)

    # Remove the second argument of sys.argv, that's the Add-on entrypoint we want to execute
    entrypoint = sys.argv.pop(0)

    # Add saké to the path
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

    # Execute the add-on code
    with open(entrypoint, 'rb') as fdesc:
        exec(compile(fdesc.read(), entrypoint, 'exec'))
