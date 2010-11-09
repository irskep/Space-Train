"""
File:           ui.py
Author:         Fred Hatfull
Description:    This class performs all UI-related management. It is responsible for drawing UI components and managing certain events fired elsewhere in the game engine.
Notes: 

UI Life Cycle:
* Instantiation should happen as soon as possible at run time. There should only be one instance of a UI object at any given time as per the Singleton pattern (shudder)
* Eventually the UI state should default to the main menu screen.
* The UI should be responsible for all transitions to and from the main menu screen.
* The UI will manage the player inventory.
* The UI will manage the CAM.
* The UI should /only/ be destroyed at exit-time.
"""

import json, pyglet

import actor, cam, gamestate, inventory, util

class UI(object):
	
    # Initialization
    def __init__(self):
        self.cam = None
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.inventory = inventory.Inventory()
        img = util.load_image(util.respath('actors', 'fist', 'stand_front.png'))
        img_data = img.get_image_data()
        img_w = img_data.width
        img_h = img_data.height
        sprite = pyglet.sprite.Sprite(img, x = gamestate.norm_w, y = gamestate.norm_h - img_h, batch=self.batch)
        self.sprites.append(sprite)
    
    def show_cam(self, actor, actions):    
        ax = actor.abs_position_x() - 180
        ay = actor.abs_position_y() + (actor.height() / 2)
        px, py = actor.scene.camera.world_to_screen_position(ax, ay)
        self.cam = cam.CAM(actions, px, py, self)
    
    def clean_cam(self):
        self.cam = None
    
    # render the UI to the screen
    def draw(self, dt=0):
        self.batch.draw()
        self.inventory.draw()
        
        if(self.cam is not None):
            self.cam.draw()
    
