import settings

import scene, scenehandler, ui

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene):
        self.scene = scene.Scene(first_scene)
        self.scene_handler = scenehandler.SceneHandler(self.scene)
        self.update = self.scene_handler.scene.update
    
    # method to draw appropriate elements
    # unsure if this change is proper (i.e. calling draw() rather than assigning a function to draw()
    # in the constructor. these are equivalent?
    def draw(self):
        self.scene_handler.scene.draw()
        ui.UI.draw()
        print ui.UI.cam