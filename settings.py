fullscreen = False

import os

def readlinkabs(l):
    """
    Return an absolute path for the destination 
    of a symlink
    """
    assert (os.path.islink(l))
    p = os.readlink(l)
    if os.path.isabs(p):
        return p
    return os.path.join(os.path.dirname(l), p)

try:
    
    from Carbon import File
    fs, _, _ = File.ResolveAliasFile('resources',1)
    resources_path = fs.as_pathname()
except ImportError:
    resources_path = readlinkabs('resources')
