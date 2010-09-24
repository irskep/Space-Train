"""
File:           scenehandler.py
Description:    Handles scene loading, saving, and transitions.
Notes: A scenehandler object has a save() method which will save all data for the scene in the autosave folder. Whenever a plot element is completed (task completed, item acquired, etc.) the save() method should be called.

When a new scene is needed or the game is closed, the notify() method should be used. If a new scene is specified then scenehandler initiates a scene transition which is completed by gamehandler. If no new scene is specified, it is assumed that the user is attempting to exit the game, and the gamehandler will be notified to allow the user to save their game before closing.
"""

import json

import pyglet

import gamestate, actionsequencer, util, interpolator

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, scene_object, game_handler, fade = 1.5):
        super(SceneHandler, self).__init__()
        self.scene = scene_object
        self.handler = game_handler
        self.save_path = util.respath('saves', 'autosave', self.scene.name)
        
        self.controller = interpolator.InterpolatorController()
        self.fade_time = fade
        self.batch = pyglet.graphics.Batch()
        
        # Build transition sprite(s)
        scene_transition_img = pyglet.resource.image(util.respath('environments', 'transitions', 'test.png'))
        self.sprite = pyglet.sprite.Sprite(scene_transition_img, x = 0, y = 0, batch=self.batch)
        self.sprite.opacity = 0
        
        gamestate.main_window.push_handlers(self.scene)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)

    # Called by a scene to load a new scene.
    def notify(self, next_scene):
        self.exit()
        self.update()
        
    # Called when exiting a scene, fades to the transition image
    def exit(self):
        """ Setup an interpolator for the opacity, fade from 0 to 255. """
        InterpClass = interpolator.LinearInterpolator
        interp = InterpClass(self.sprite, 'opacity', end = 255, start = 0, 
                             duration=self.fade_time, done_function=self.update) # Should be a no-op for now
        self.controller.add_interpolator(interp)
        
    def enter(self):
        InterpClass = interpolator.LinearInterpolator
        interp = InterpClass(self.sprite, 'opacity', end = 0, start = 255,
                             duration = self.fade_time, done_function=self.update)
        self.controller.add_interpolator(interp)
    
    def update(self, dt=0):
        self.controller.update_interpolators(dt)
        self.scene.update(dt)
    
    def draw(self):
        self.batch.draw()