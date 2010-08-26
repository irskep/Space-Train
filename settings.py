fullscreen = False

try:
    from Carbon import File
    fs, _, _ = File.ResolveAliasFile('resources',1)
    resources_path = fs.as_pathname()
except ImportError:
    try:
        # Delete this line and replace it with Windows shortcut-following code
        raise ImportError
    except ImportError:
        resources_path = 'resources'
