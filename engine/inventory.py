"""
File:           inventory.py
Author:         Fred Hatfull
Description:    This class is responsible for managing and providing a graphical representation of a player's inventory. It should be managed by the UI class.
Notes: 

Inventory Life Cycle:
* Inventory should be instantiated with UI and should also follow the conventions of the singleton pattern (i.e. only one inventory object should ever exist).
* Inventory should be capable of tracking a player's objects throughout his/her game. 
* Inventory should manifest itself graphically as either an icon (closed) or an icon with a lengthy background upon which a player's items are displayed (open)
* Inventory should provide facilities for adding items to the inventory or sending items in the inventory to the game world (drag & drop)
* Inventory should be destroyed with UI at shutdown
"""


import copy

import json, pyglet

import gamestate, util

class Inventory(object):

    # Initialization
    def __init__(self):
        self.sprites = {}
        self.images = []
        self.batches = {}
        self.batches['open'] = pyglet.graphics.Batch()
        self.batches['closed'] = pyglet.graphics.Batch()
        self.sprites['open'] = {}
        self.sprites['closed'] = []
        
        self.width = 5
        
        # Create the inventory closed state first
        # i know this is dirty, shut up!
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_left.png'], x = gamestate.norm_w + x, y = gamestate.norm_h,  batch = self.batches['closed']) )
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_mid.png'], x = gamestate.norm_w + x, y = gamestate.norm_h, batch = self.batches['closed']) )
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_right.png'], x = gamestate.norm_w + x, y = gamestate.norm_h, batch = self.batches['closed']) )
                
        # translate everything to where it needs to be
        x_trans = 0
        y_trans = 0
        for sprite in self.sprites['closed']:
            x_trans += sprite.width
            y_trans = sprite.height

        for sprite in self.sprites['closed']:
            sprite.x -= x_trans
            sprite.y -= y_trans
            print "Sprite at (%d, %d)" % (sprite.x, sprite.y)
        
        self.isopen = False
        
      
        # Create the inventory open state now
        self.set_inventory_ui_width(5)
    
        gamestate.main_window.push_handlers(self)
            
    # used for (re)sizing the inventory UI open state. right now takes width as a number of intermediate middle sections to show; when real gfx are in it should be in px
    def set_inventory_ui_width(self, width):
        sprites = {}
        sprites['mid'] = []
        
        x = 0
        sprites['left'] = util.load_sprite(['ui', 'inventory_left.png'], x = gamestate.norm_w, y = gamestate.norm_h, batch = self.batches['open'])
        x += sprites['left'].width

        while(width > 0):
            sprites['mid'].append( util.load_sprite(['ui', 'inventory_mid.png'], x = gamestate.norm_w, y = gamestate.norm_h, batch = self.batches['open']) )
            sprites['mid'][-1].x += x
            x += sprites['mid'][-1].width
            width -= 1
        
        sprites['right'] = util.load_sprite(['ui', 'inventory_right.png'], x = gamestate.norm_w + x, y = gamestate.norm_h, batch = self.batches['open'])
        x += sprites['right'].width
        
        y = sprites['left'].height
        
        self.sprites['open'] = []
        self.sprites['open'].append(sprites['left'])
        self.sprites['open'].append(sprites['right'])
        self.sprites['open'].extend(sprites['mid'] )
        for sprite in self.sprites['open']:
            sprite.x -= x
            sprite.y -= y
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.intersects_active_area(x, y):
            self.toggle()
            return pyglet.event.EVENT_HANDLED
        else:
            return pyglet.event.EVENT_UNHANDLED
            
    
    def toggle(self):
        self.isopen = not self.isopen
        
    def intersects_active_area(self, x, y):
        sprite_list = (self.sprites['open'] if self.isopen else self.sprites['closed'])
        for sprite in sprite_list:
            if(x > sprite.x and x < sprite.x + sprite.width and
               y > sprite.y and y < sprite.y + sprite.height):
                return True
        return False 
        
    # Render the inventory in the UI
    def draw(self, dt=0):
        #print self.isopen
        if(self.isopen is False):
            self.batches['closed'].draw()
        else:
            self.batches['open'].draw()