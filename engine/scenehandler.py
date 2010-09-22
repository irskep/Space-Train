import json

import pyglet

import gamestate, actionsequencer

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, scene_object):
        super(SceneHandler, self).__init__()
        self.scene = scene_object
        self.save_path = util.respath_func_with_base_path('game', 'saves', self.name)
        gamestate.main_window.push_handlers(self.scene)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)
      
    # Called by a scene to load a new scene.
    # If exit = 1 then we are exiting the current game.
    def notify(next_scene, exit = 0):
        return 0
