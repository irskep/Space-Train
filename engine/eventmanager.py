"""
File:           eventmanager.py
Description:    This class is responsible for maintaining event handlers on the pyglet event stack in the proper order.
Notes: 

This class should manage placement in the event stack of the following objects:
* Scene
* Inventory
* CAM

To manage your events, (TODO)
"""

import pyglet
import cam, gamestate, scene

#HAH-HA!!
#I GET TO USE CAMELCASE!
class EventManager(object):
    
    def __init__(self, scene = None, inventory = None, cam = None):
        self.scene = scene
        self.inventory = inventory
        self.cam = cam
        self.build_stack()
        
    # build the event stack in the correct order needed for SPACE TRAIIIN
    def build_stack(self):
        self.clear_stack()

        #here is where the order of event handlers is determined
        self.add_handlers(pyglet.window.key.KeyStateHandler())
        self.add_handlers(self.scene)
        self.add_handlers(self.inventory)
        self.add_handlers(self.cam)
    
    # methods to set certain objects
    # will rebuild the stack when called
    def set_scene(self, scene):
        self.scene = scene
        self.build_stack()
        
    def set_inventory(self, inventory):
        self.inventory = inventory
        self.build_stack()
        
    def set_cam(self, cam):
        self.cam = cam
        self.build_stack()
    
    # Clear the event handler stack
    def clear_stack(self):
        # A very hacky way to do this. In the future we can count the levels on the stack,
        # although that makes the assumption that handlers won't be pushed or popped by other sources
        while True:
            try:
                gamestate.main_window.pop_handlers()
            except AssertionError:
                break
    
    # A convenience method to shorten gamestate.main_window.push_handlers()
    def add_handlers(self, obj):
        if(obj is not None):
            gamestate.main_window.push_handlers(obj)