"""
Usage:
    python setup.py py2app
"""

from setuptools import setup
OPTIONS = dict(
    argv_emulation=True,
    frameworks=[],
    plist = dict(CFBundleIconFile='spacetrain.icns'), 
    # PyRuntimeLocations=['/Library/Frameworks/Python.framework/Versions/Current/Python']
    #, '/System/Library/Frameworks/Python.framework/Versions/Current/Python'])
)

setup(
    name='Space Train',
    app=['Adventure.py'],
    data_files=['engine','resources', 'game', 'spacetrain.icns',
                'glydget', 'yaml', 'pyglet'],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)