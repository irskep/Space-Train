"""
File:           gamehandler.py
Description:    Handles game loading, saving, and initilization.
Notes:
"""

import gamestate

import scene, scenehandler, ui

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene):
        self.ui = ui.UI()

        self.scene_handler = scenehandler.SceneHandler(first_scene, self)
        self.update = self.scene_handler.update
        
    # Called by scenehandler when the user is exiting the game, should prompt for a save
    def notify(self):
        pass
    
    # method to draw appropriate elements
    # unsure if this change is proper (i.e. calling draw() rather than assigning a function to draw()
    # in the constructor. these are equivalent?
    
    @gamestate.scaled
    def draw(self, dt=0):
        self.scene_handler.scene.draw()
        self.ui.draw()
        self.scene_handler.draw()