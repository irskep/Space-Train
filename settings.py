fullscreen = False

try:
    from Carbon import File
    fs, _, _ = File.ResolveAliasFile('resources',1)
    resources_path = fs.as_pathname()
except ImportError:
    resources_path = 'resources'
