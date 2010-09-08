import json

import pyglet

import gamestate

class SceneHandler(object):
    def __init__(self, scene_object):
        self.scene = scene_object
        gamestate.main_window.push_handlers(self.scene)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)