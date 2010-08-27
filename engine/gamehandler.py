import settings, state

import scene

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene):
        self.scene = scene.Scene(first_scene)
        self.update = self.scene.update
        self.draw = self.scene.draw
    
