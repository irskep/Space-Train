fullscreen = False

import os

resource_locations = [
    r"resources",   # the 'r' turns off escape sequences
    r"C:\Users\Fred\Documents\My Dropbox\resources",
    r"YOUR_PATH_HERE"
]

for location in resource_locations:
    if os.path.isdir(location):
        resources_path = location
        break
    else:
        try:
            from Carbon import File
            fs, _, _ = File.ResolveAliasFile('resources',1)
            resources_path = fs.as_pathname()
            break
        except:
            pass
