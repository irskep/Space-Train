from engine import actor

myscene = None

def init(scn, env):
    """Your opportunity to initialize a subclass of SceneHandler"""
    pass

def scene_loaded():
    print "I made a", myscene
