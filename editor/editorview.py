import pyglet

from engine import scene, gamestate

import sidebar

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        self.sidebar = sidebar.Sidebar()
        gamestate.sidebar_w = self.sidebar.width
        self.sidebar.push_handlers()
    
    def draw(self):
        self.scene.draw()
        self.sidebar.draw()
    

