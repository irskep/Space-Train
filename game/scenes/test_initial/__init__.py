from engine import actor, scenehandler

scene_handler = None

def init(scene_obj, env):
    """Your opportunity to initialize a subclass of SceneHandler"""
    pass

def scene_loaded():
    print "I made a", scene_handler
