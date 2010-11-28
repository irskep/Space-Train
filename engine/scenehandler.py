"""
File:           scenehandler.py
Description:    Handles scene loading, saving, and transitions.
Notes: A scenehandler object has a save() method which will save all data for the scene in the autosave folder. Whenever a plot element is completed (task completed, item acquired, etc.) the save() method should be called.

When a new scene is needed or the game is closed, the notify() method should be used. If a new scene is specified then scenehandler initiates a scene transition. If no new scene is specified, it is assumed that the user is attempting to exit the game, and the gamehandler will be notified to allow the user to save their game before closing.
"""

import os
import json
import functools

import pyglet

import gamestate, actionsequencer, util, interpolator, scene

NONE = 0
FADE = 1
UP = 2
RIGHT = 3
DOWN = 4
LEFT = 5

class SceneHandler(actionsequencer.ActionSequencer):
    def __init__(self, game_handler):
        super(SceneHandler, self).__init__()
        self.scene = None   # Main scene
        self.scenes = []    # Scenes to be drawn
        self.handler = game_handler
        
        self.controller = interpolator.InterpolatorController()
        self.fade_time = 1.0
        self.batch = pyglet.graphics.Batch()
        
        # Build transition sprite(s)
        scene_transition_img = util.load_image(util.respath('environments', 'transitions', 'test.png'))
        self.sprite = pyglet.sprite.Sprite(scene_transition_img, x = 0, y = 0, batch=self.batch)
        self.sprite.opacity = 0
    
    def set_first_scene(self, scn):
        self.set_scenes(scn)
        gamestate.event_manager.set_scene(self.scene)
    
    def set_scenes(self, *args):
        if args:
            self.scene = args[0]
        else:
            self.scene = None
        self.scenes = args
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s)" % str(self.scene)
    
    def make_or_load_scene(self, scene_name):
        p = os.path.join(self.handler.save_path, 'autosave', scene_name)
        if os.path.exists(p + '.json'):
            return scene.Scene(scene_name, self, self.handler.ui, load_path=p)
        else:
            return scene.Scene(scene_name, self, self.handler.ui)

    # Called by a scene to load a new scene.
    # If dir is specified a sliding transition is used
    def notify(self, next_scene, direction=FADE):
        if self.handler.ui.cam is not None:
            self.handler.ui.cam.set_visible(False)
        
        if next_scene is None:
            self.handler.prompt_save_and_quit()
        else:
            self.handler.save()
            if direction == FADE:
                self.fade_to(next_scene)
            elif direction == NONE:
                gamestate.event_manager.set_scene(None)
                self.scene.exit()
                new_scene = self.make_or_load_scene(make_or_load_scene)
                new_scene.transition_from(self.scene.name)
                self.set_scenes(new_scene)
                gamestate.event_manager.set_scene(self.scene)
            else:
                self.slide_to(next_scene, direction)
            
    # For direction 1 is up, 2 is right, 3 is down, 4 is left
    def slide_to(self, next_scene, direction=RIGHT):
        InterpClass = interpolator.LinearInterpolator
        gamestate.event_manager.set_scene(None)
        slide_scene = self.make_or_load_scene(next_scene)
        slide_scene.pause(show_sprites=False)
        self.set_scenes(self.scene, slide_scene)
        # Determine offset
        if direction == UP:
            slide_scene.y_offset = gamestate.norm_h
        elif direction == RIGHT:
            slide_scene.x_offset = gamestate.norm_w
        elif direction == DOWN:
            slide_scene.y_offset = -gamestate.norm_h
        elif direction == LEFT:
            slide_scene.x_offset = -gamestate.norm_w
        
        def slide(ending_action=None):
            self.scene.pause(show_sprites=False)
            if direction % 2:   # Up/down
                interp1 = InterpClass(self.scene, 'y_offset', 
                                      end=-slide_scene.y_offset, 
                                      duration=2*self.fade_time)
                interp2 = InterpClass(slide_scene, 'y_offset', 
                                      end=0, duration=2*self.fade_time,
                                      done_function=self.next_action())
            else:               # Left/right
                interp1 = InterpClass(self.scene, 'x_offset', start=0, 
                                      end=-slide_scene.x_offset, 
                                      duration=2*self.fade_time)
                interp2 = InterpClass(slide_scene, 'x_offset', 
                                      end=0, duration=2*self.fade_time, 
                                      done_function=self.next_action)
                slide_scene.x_offset = gamestate.norm_w
                
            self.controller.add_interpolator(interp1)
            self.controller.add_interpolator(interp2)
            
        def complete_transition(ending_action=None):
            self.handler.save()
            self.scene.exit()
            slide_scene.transition_from(self.scene.name)
            self.set_scenes(slide_scene)
            self.scene.resume()    
            gamestate.event_manager.set_scene(self.scene)
            self.next_action()
            
        self.simple_sequence(slide, complete_transition)
    
    def fade_to(self, next_scene):
        InterpClass = interpolator.LinearInterpolator
        def fade_out(ending_action=None):
            gamestate.event_manager.set_scene(None)
            interp = InterpClass(self.sprite, 'opacity', end=255, start=0, duration=self.fade_time,
                                done_function=self.next_action)
            self.controller.add_interpolator(interp)
        
        def complete_transition(new_scene, ending_action=None):
            gamestate.event_manager.set_scene(self.scene)
            new_scene.resume()
            self.next_action()
        
        def fade_in(ending_action=None):
            # Remove scene
            self.handler.save()
            self.scene.exit()
            new_scene = self.make_or_load_scene(next_scene)
            new_scene.transition_from(self.scene.name)
            new_scene.pause(show_sprites=False)
            
            # An ever-increasing pile of hax
            for i in xrange(10):
                new_scene.zenforcer.update()
            
            self.set_scenes(new_scene)
            interp = InterpClass(self.sprite, 'opacity', end=0, start=255, duration=self.fade_time,
                                done_function=functools.partial(complete_transition, new_scene))
            self.controller.add_interpolator(interp)
        
        self.simple_sequence(fade_out, fade_in)
    
    def update(self, dt=0):
        if dt > 0.2:
            dt = 0.01
        self.controller.update_interpolators(dt)
        
        # DIRTY DIRTY DIRTY (to save a function call)
        self.handler.dj.update(dt)
        self.handler.background_dj.update(dt)
        
        for scn in self.scenes:
            scn.update(dt)
    
    def draw_scenes(self):
        for scn in self.scenes:
            scn.draw()
    
    def draw(self):
        self.batch.draw()
    
