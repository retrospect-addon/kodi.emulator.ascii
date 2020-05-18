# SPDX-License-Identifier: GPL-3.0

import os.path

import __init__
from setuptools import setup

project_dir = os.path.dirname(os.path.abspath(__file__))


setup(
    name='sake',
    version=0.1,
    url='https://github.com/retrospect-addon/kodi.emulator.ascii',
    author='Bas Rieter',
    description='SAKÉ can help you to debug and develop Kodi Python add-ons',
    long_description=open(os.path.join(project_dir, 'README.md')).read(),
    keywords='Kodi, emulator, ascii',
    license='GPL-3.0',
    py_modules=__init__.__all__,
    zip_safe=False,
)
