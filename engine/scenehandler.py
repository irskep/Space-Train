"""
File:           scenehandler.py
Description:    Handles scene loading, saving, and transitions.
Notes: A scenehandler object has a save() method which will save all data for the scene in the autosave folder. Whenever a plot element is completed (task completed, item acquired, etc.) the save() method should be called.

When a new scene is needed or the game is closed, the notify() method should be used. If a new scene is specified then scenehandler initiates a scene transition. If no new scene is specified, it is assumed that the user is attempting to exit the game, and the gamehandler will be notified to allow the user to save their game before closing.
"""

import json

import pyglet

import gamestate, actionsequencer, util, interpolator, scene

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, scene_name, game_handler, fade = 1.0):
        super(SceneHandler, self).__init__()
        self.scene = scene.Scene(scene_name, self, game_handler.ui)
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
        if self.handler.ui.cam is not None:
            self.handler.ui.cam.visible = False
        self.update()
        
        # Remove scene
        self.save()
        
        if next_scene is None:
            # Notify game handler, we are exiting
            self.handler.notify()
        else:
            self.fade_to(next_scene)
    
    def fade_to(self, next_scene):
        new_scene = scene.Scene(next_scene, self.handler.ui)
        
        InterpClass = interpolator.LinearInterpolator
        def fade_out(ending_action=None):
            gamestate.main_window.pop_handlers()
            interp = InterpClass(self.sprite, 'opacity', end=255, start=0, duration=self.fade_time,
                                done_function=self.next_action)
            self.controller.add_interpolator(interp)
        
        def complete_transition(ending_action=None):
            gamestate.main_window.push_handlers(self.scene)
            self.next_action()
        
        def fade_in(ending_action=None):
            self.scene.exit()
            new_scene.transition_from(self.scene.name)
            self.scene = new_scene
            interp = InterpClass(self.sprite, 'opacity', end=0, start=255, duration=self.fade_time,
                                done_function=complete_transition)
            self.controller.add_interpolator(interp)
        
        self.simple_sequence(fade_out, fade_in)
    
    # Initiates an autosave
    def save(self):
        pass
    
    def update(self, dt=0):
        self.controller.update_interpolators(dt)
        self.scene.update(dt)
    
    def draw(self):
        self.batch.draw()
    
