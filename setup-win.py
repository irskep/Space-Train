"""
Usage (Mac):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe
"""

import sys, os, re, pdb
from distutils.core import setup
import py2exe

def grab_files(loc, current_folder=''):
    data_files = []
    file_list = []
    reg = re.search('\\\\([^\\\\]+)\\\\?$', loc)
    folder = current_folder + '\\'
    for file in os.listdir(loc):
        f1 = loc + '\\' + file
        if not os.path.isdir(f1):
            file_list.append(f1)
        else:
            data_files.extend(grab_files(f1, current_folder = folder + reg.group(1)))
    data_files.append((folder, file_list))
    return data_files

mainscript = 'Adventure.py'

OPTIONS = dict(
    argv_emulation=True,
    frameworks=[],
    plist = dict(CFBundleIconFile='spacetrain.icns'), 
    # PyRuntimeLocations=['/Library/Frameworks/Python.framework/Versions/Current/Python']
    #, '/System/Library/Frameworks/Python.framework/Versions/Current/Python'])
)
extra_options = dict(
    setup_requires=['py2exe'],
    app=[mainscript],
)

loc = ["C:\Users\Tyler\Documents\College\Space-Train\engine", "C:\Users\Tyler\Documents\College\Space-Train\game",
       "C:\Users\Tyler\Documents\College\Space-Train\glydget", "C:\Users\Tyler\Documents\My Dropbox\\resources",
       "C:\Python27\Lib\site-packages\yaml", "C:\Python27\Lib\site-packages\pyglet"]
Mydata_files = []
for i in range(0, len(loc)):
    Mydata_files.extend(grab_files(loc[i], re.search('\\\\[^\\\\]+$', loc[i]).group(0)))

f = open('out.txt', 'w')
for item in Mydata_files:
    print >>f, item

setup(
    console=[mainscript],
    #data_files=Mydata_files,
    **extra_options
)