import settings, state

import scene

class GameHandler(object):
    def __init__(self, first_scene):
        self.scene = scene.Scene(first_scene)
        self.update = self.scene.update
    
    def draw(self):
        self.scene.env.draw()
    
