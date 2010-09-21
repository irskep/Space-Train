"""
File:           cam.py
Author:         Fred Hatfull
Description:    A class encompassing the primary functionality of the Contextual Action Menu (CAM) in SPACE TRAIN.
Notes: 

Contextual Action Menu Life Cycle:
* A CAM instance is requested by a caller (scene, object, level script, something)
    * The caller must provide:
        + A reference to the UI object in use (will probably be a singleton/global)
        + A dictionary of available actions: {'action_name': [function or closure]}
        + A coordinate indicating the centre of menu area around which actions will appear
* A CAM is instantiated and attached to the UI object
    * When a CAM is instantiated it will not have to load any resources like sprites - these should be allocated as static resources somehow and associated with the CAM when it is created
* The CAM is set to visible to indicate that it should drawn by the UI each frame at the specified coordinates
* The CAM remains visible until it detects a click:
    * If the click is within a region controlled by the CAM (i.e. on an action button), the CAM calls the callback associated with the action
    * If the click is elsewhere, pass the event down the event stack and set the CAM to false.
        * Destroy the CAM instance?
"""

import copy
import json, pyglet
import gamestate, ui, util

# Static resources, such as sprites for the CAM backgrounds
sprites = {}
sprite_batch = pyglet.graphics.Batch()
sprites['action_background'] = util.loadSprite(['ui', 'cam_item.png'], 0, 0, sprite_batch)

class CAM(object):
    
    # Init
    def __init__(self, ui, actions, x, y):
        self.visible = False
        ui.cam = self
        self.actions = actions
        self.x = x
        self.y = y
        self.visible = True
        gamestate.main_window.push_handlers(self)
        
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.labels = []
        
        sprites['action_background'].batch = self.batch
        
        # Turn each action entry into a menu item
        # TODO: turn this mess into a function/class
        for action, callback in self.actions.items():
            # set up the background sprite
            new_sprite = copy.copy(sprites['action_background'])
            new_sprite.batch = self.batch
            new_sprite.x = x #??
            new_sprite.y = y #??
            self.sprites.append(new_sprite)
            
            # set up the label for the menu item
            new_label = pyglet.text.Label(action, font_name = 'Times New Roman', font_size = 12, x = new_sprite.x + 5, y = new_sprite.y + 3, anchor_x = 'left', anchor_y = 'center', batch = self.batch)
            self.labels.append(new_label)
            
    # Handle an event
    def on_mouse_release(self, x, y, button, modifiers):
        print "Mouse press!"
        return False
    
    def draw(self):
        print "HAI"
        if(self.visible):
            print "Should be drawing"
            self.batch.draw()