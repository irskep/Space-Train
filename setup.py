"""
Usage (Mac):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

import sys

mainscript = 'Adventure.py'

OPTIONS = dict(
    argv_emulation=True,
    frameworks=[],
    plist = dict(CFBundleIconFile='spacetrain.icns'), 
    # PyRuntimeLocations=['/Library/Frameworks/Python.framework/Versions/Current/Python']
    #, '/System/Library/Frameworks/Python.framework/Versions/Current/Python'])
)

if sys.platform == 'darwin':
     from setuptools import setup
     extra_options = dict(
         setup_requires=['py2app'],
         app=[mainscript],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
         options={'py2app': OPTIONS},
     )
elif sys.platform == 'win32':
     from distutils.core import setup
     import py2exe
     extra_options = dict(
         setup_requires=['py2exe'],
         app=[mainscript],
     )
else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[mainscript],
     )

setup(
    name='Space Train',
    data_files=['engine','resources', 'game', 'spacetrain.icns',
                'glydget', 'yaml', 'pyglet'],
    **extra_options
)