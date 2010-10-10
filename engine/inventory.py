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
        self.sprites['open'] = []
        self.sprites['closed'] = []

        self.batches['items'] = pyglet.graphics.Batch()
        
        self.items = {}
        
        self.width = 5
                
        self.isopen = False
        
        # Create the inventory closed state first
        self.sprites['closed'].append( util.load_sprite(['ui', 'purse.png'], x = gamestate.norm_w, y = gamestate.norm_h, batch = self.batches['closed']) )
        self.translate_bottomleft_to_topright(self.sprites['closed'])
                      
        # Create the inventory open state now
        self.sprites['open'].append( util.load_sprite(['ui', 'purseopen.png'], x = gamestate.norm_w, y = gamestate.norm_h, batch = self.batches['open']) )
        self.translate_bottomleft_to_topright(self.sprites['open'])

        gamestate.event_manager.set_inventory(self)
    
    # inventory item interaction methods
    def put_item(self, actor):
        self.items[actor.identifier] = actor
        self.items[actor.identifier].sprite.batch = self.batches['items']
        self.update_item_positions()

    def get_item(self, identifier):
        self.items[identifier].sprite.batch = self.items[identifier].scene.batch
        ret = self.items[identifier]
        del self.items[identifier]
        self.update_item_positions()
        return ret
        
    def update_item_positions(self):
        leftmost_x = self.sprites['open'][0].x
        inventory_height = self.sprites['open'][0].height
        inventory_y = self.sprites['open'][0].y
        for ident, item in self.items.iteritems():
            sprite = item.sprite
            # place the sprite appropriately
            sprite.x = leftmost_x - sprite.width
            sprite.y = inventory_y
            print "Sprite %s dimensions (%d, %d) position (%d, %d)" % (ident, sprite.width, sprite.height, sprite.x, sprite.y)
            leftmost_x -= sprite.width
    
    #needs to go in util sometime
    def translate_bottomleft_to_topright(self, sprites):
        # translate everything to where it needs to be
        x_trans = 0
        y_trans = 0
        for sprite in sprites:
            x_trans += sprite.width
            y_trans = sprite.height
        for sprite in sprites:
            sprite.x -= x_trans
            sprite.y -= y_trans
    
    def on_mouse_release(self, x, y, button, modifiers):
        print "Inventory handling click at (%d, %d)" % (x, y)
        if self.intersects_active_area(x, y):
            print "clix"
            if(util.intersects_sprite(x, y, self.sprites['closed'][0])):
                self.toggle()
            return pyglet.event.EVENT_HANDLED
        else:
            return pyglet.event.EVENT_UNHANDLED
            
    
    def toggle(self):
        self.isopen = not self.isopen
        
    def intersects_active_area(self, x, y):
        sprite_list = []
        sprites = (self.sprites['open'] if self.isopen else self.sprites['closed'])
        sprite_list.extend(sprites)
        for sprite in sprite_list:
            if(x > sprite.x and x < sprite.x + sprite.width and
               y > sprite.y and y < sprite.y + sprite.height):
                return True
                
        if self.isopen:
            for id, item in self.items.iteritems():
                if item.covers_point(x, y):
                    return True
        return False 
        
    # Render the inventory in the UI
    def draw(self, dt=0):
        #print self.isopen
        if(self.isopen is False):
            self.batches['closed'].draw()
        else:
            self.batches['open'].draw()
            self.batches['items'].draw()