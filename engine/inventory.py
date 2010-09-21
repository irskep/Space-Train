"""Dear Fred, 
Please do not use camelCase. I have signficant butthurt about this issue. 

Sincerely, 
Steve."""

import copy

import json, pyglet

import gamestate, settings, util

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
        
        # Create the inventory closed state first
        # i know this is dirty, shut up!
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_left.png'], gamestate.norm_w + x, gamestate.norm_h, self.batches['closed']) )
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_mid.png'], gamestate.norm_w + x, gamestate.norm_h, self.batches['closed']) )
        x = 0
        for sprite in self.sprites['closed']:
            x += sprite.width
        self.sprites['closed'].append( util.load_sprite(['ui', 'inventory_right.png'], gamestate.norm_w + x, gamestate.norm_h, self.batches['closed']) )
                
        # translate everything to where it needs to be
        x_trans = 0
        y_trans = 0
        for sprite in self.sprites['closed']:
            x_trans += sprite.width
            y_trans = sprite.height

        for sprite in self.sprites['closed']:
            sprite.x -= x_trans
            sprite.y -= y_trans
        
        self.isopen = False
        
        
        # Create the inventory open state now
        self.sprites['open']['mid'] = []
        
        x = 0
        self.sprites['open']['left'] = util.load_sprite(['ui', 'inventory_left.png'], gamestate.norm_w, gamestate.norm_h, self.batches['open'])
        x += self.sprites['open']['left'].width
        midsprite = util.load_sprite(['ui', 'inventory_mid.png'], gamestate.norm_w, gamestate.norm_h, self.batches['open'])
        self.sprites['open']['mid'].append(copy.deepcopy(midsprite))
        self.sprites['open']['mid'][-1].x += x
        x += self.sprites['open']['mid'][-1].width
        self.sprites['open']['mid'].append(copy.deepcopy(midsprite))
        self.sprites['open']['mid'][-1].x += x
        x += self.sprites['open']['mid'][-1].width
        self.sprites['open']['right'] = util.load_sprite(['ui', 'inventory_right.png'], gamestate.norm_w + x, gamestate.norm_h, self.batches['open'])
        x += self.sprites['open']['right'].width
        
        y = self.sprites['open']['left'].height
        
        open_sprites = []
        open_sprites.append(self.sprites['open']['left'])
        open_sprites.append(self.sprites['open']['right'])
        open_sprites.extend( self.sprites['open']['mid'] )
        for sprite in open_sprites:
            sprite.x -= x
            sprite.y -= y
            print "Sprite: %s x:%d y:%d b:%s" % (sprite, sprite.x, sprite.y, sprite.batch)
        
        gamestate.main_window.push_handlers(self)
        
    def on_mouse_release(self, x, y, button, modifiers):
        return False
        if self.intersects_active_area(x, y):
            self.toggle()
            return pyglet.event.EVENT_HANDLED
        else:
            return False
            
    
    def toggle(self):
        self.isopen = not self.isopen
        
    def intersects_active_area(self, x, y):
        return True
        
    # Render the inventory in the UI
    def draw(self):
        if(self.isopen is False):
            self.batches['closed'].draw()
        else:
            self.batches['open'].draw()