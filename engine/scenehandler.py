import json

import pyglet

import gamestate, actionsequencer

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, scene_object):
        super(self, SceneHandler).__init__()
        self.scene = scene_object
        gamestate.main_window.push_handlers(self.scene)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)