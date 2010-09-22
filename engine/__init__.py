import os, sys, pyglet

import settings

#Bootstrap's bootstraps

resource_locations = [
    os.path.join(os.path.dirname(__file__), r"resources"),   # the 'r' turns off escape sequences
    r"C:\Users\Fred\Documents\My Dropbox\resources",
    r"/Users/stephen/Dropbox/resources",
    r"C:\Users\Tyler\Documents\My Dropbox\resources"
]

for location in resource_locations:
    if os.path.isdir(location):
        settings.resources_path = location
        break
    else:
        try:
            from Carbon import File
            fs, _, _ = File.ResolveAliasFile('resources',1)
            settings.resources_path = fs.as_pathname()
            break
        except:
            pass

pyglet.resource.path.append(settings.resources_path)
pyglet.resource.path.append(os.getcwd())
pyglet.resource.reindex()


def nested_image(*args):
    return pyglet.resource.image('/'.join(args))

pyglet.resource.nested_image = nested_image