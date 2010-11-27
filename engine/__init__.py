import os, sys, pyglet

from util import settings

#Bootstrap's bootstraps

def init():
    resource_locations = [
        r"resources",
        r"C:\Users\Fred\Documents\My Dropbox\resources",
        r"/Users/stephen/Dropbox/resources",
        r"C:\Users\Tyler\Documents\My Dropbox\resources",
        r"C:\Users\merfie\Documents\My Dropbox\resources"
    ]

    try:
        more_locations = [
            os.path.join(os.path.dirname(sys.argv[0]), r"resources"),
            os.path.join(os.path.dirname(sys.argv[0]), r"resources_repo"),
        ]
        resource_locations = more_locations + resource_locations
    except:
        pass

    for location in resource_locations:
        if os.path.isdir(location):
            settings.resources_path = location
            break
        else:
            try:
                from Carbon import File
                fs, _, _ = File.ResolveAliasFile('location',1)
                settings.resources_path = fs.as_pathname()
                break
            except:
                pass

    pyglet.resource.path.append(settings.resources_path)
    pyglet.resource.path.append(os.getcwd())
    pyglet.resource.reindex()
