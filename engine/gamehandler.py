import settings

import scene, scenehandler

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene):
        self.scene = scene.Scene(first_scene)
        self.scene_handler = scenehandler.SceneHandler(self.scene)
        self.update = self.scene_handler.scene.update
        self.draw = self.scene_handler.scene.draw
    
