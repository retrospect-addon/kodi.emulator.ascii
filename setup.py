# coding=utf-8  # NOSONAR
# SPDX-License-Identifier: GPL-3.0
import io
import os.path
from setuptools import setup

project_dir = os.path.dirname(os.path.abspath(__file__))


setup(
    name='sakee',
    version="0.0.13",
    url='https://github.com/retrospect-addon/kodi.emulator.ascii',
    author='Bas Rieter',
    description='SAKÉ can help you to debug and develop Kodi Python add-ons',
    long_description=io.open(os.path.join(project_dir, 'README.md'), encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    keywords='Kodi, emulator, ascii, xbmc, xbmcgui, xbmcplugin, xbmcaddon',
    license='GPL-3.0',
    py_modules=["xbmc", "xbmcgui", "xbmcaddon", "xbmcgui", "inputstreamhelper", "xbmcplugin", "xbmcvfs"],
    packages=["sakee"],
    project_urls={
        'Documentation': 'https://github.com/retrospect-addon/kodi.emulator.ascii/blob/master/README.md',
        'Source': 'https://github.com/retrospect-addon/kodi.emulator.ascii/',
        'Tracker': 'https://github.com/retrospect-addon/kodi.emulator.ascii/issues',
    },
    zip_safe=False,
    python_requires='>=2.7'
)
