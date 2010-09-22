import gamestate

import scene, scenehandler, ui

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene):
        self.ui = ui.UI()
        self.scene = scene.Scene(first_scene, self.ui)
        self.scene_handler = scenehandler.SceneHandler(self.scene)
        self.update = self.scene_handler.scene.update
    
    # method to draw appropriate elements
    # unsure if this change is proper (i.e. calling draw() rather than assigning a function to draw()
    # in the constructor. these are equivalent?
    
    @gamestate.scaled
    def draw(self, dt=0):
        self.scene_handler.scene.draw()
        self.ui.draw()