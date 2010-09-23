"""
File:           scenehandler.py
Author:         Tyler Goeringer
Description:    Handles scene loading, saving, and transitions.
Notes: A scenehandler object has a save() method which will save all data for the scene in the autosave folder. Whenever a plot element is completed (task completed, item acquired, etc.) the save() method should be called.

When a new scene is needed or the game is closed, the notify() method should be used. If a new scene is specified then scenehandler initiates a scene transition which is completed by gamehandler. If no new scene is specified, it is assumed that the user is attempting to exit the game, and the gamehandler will be notified to allow the user to save their game before closing.
"""

import json

import pyglet

import gamestate, actionsequencer, util, interpolator

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, scene_object):
        super(SceneHandler, self).__init__()
        self.scene = scene_object
        self.save_path = util.respath('saves', 'autosave', self.scene.name)
        
        self.scene_transition_img = pyglet.resource.image(util.respath('environments', 'transitions', 'test.png'))
        self.scene_transition = SceneTransition(img = self.scene_transition_img)
        
        gamestate.main_window.push_handlers(self.scene)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)
      
    # Called by a scene to load a new scene.
    def notify(next_scene):
        return 0
        
class SceneTransition(object):
    """ Provides transitions between scenes. Currently only a fade in image. """
    def __init__(self, img, fade_time = 5.0, batch=None):
        self.controller = interpolator.InterpolatorController()
        self.fade = fade_time
        if batch is None:
            batch = pyglet.graphics.Batch()
        self.batch = batch
        self.sprite = pyglet.sprite.Sprite(img, x = 0, y = 0, batch=self.batch)
        self.sprite.opacity = 255
        print "Initializing transition."
        print "Opacity: %d Visible: %s X: %d Y: %d" % (self.sprite.opacity, self.sprite.visible, 
                                                       self.sprite.x, self.sprite.y)
        print self.sprite.image
        
    def begin(self):
        print "Beginning!"
        """ Setup an interpolator for the opacity, fade from 0 to 255. """
        InterpClass = interpolator.LinearInterpolator
        interp = InterpClass(self.sprite, 'opacity', end = 255, start = 0, 
                             duration=self.fade, done_function=self.notify)
        self.controller.add_interpolator(interp)
                             
    def notify(self):
        self.sprite.opacity = 0;
    
    def draw(self):
        self.sprite.draw()