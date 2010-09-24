import json, pyglet

import actor, cam, gamestate, inventory, util

class UI(object):
	
    # Initialization
    def __init__(self):
        self.cam = None
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.inventory = inventory.Inventory()
        img = pyglet.resource.image(util.respath('actors', 'fist', 'stand_front.png'))
        img_data = img.get_image_data()
        img_w = img_data.width
        img_h = img_data.height
        sprite = pyglet.sprite.Sprite(img, x = gamestate.norm_w, y = gamestate.norm_h - img_h, batch=self.batch)
        self.sprites.append(sprite)
	
    # handle an actor being clicked
    def actor_clicked(self, actor):
        x = actor.abs_position_x() + actor.width()
        y = actor.abs_position_y() + (actor.height() / 2)
        self.cam = cam.CAM({'Action':None, 'Action2':None, 'Action3':None, 'Action4':None, 'Action5':None, 'Action6':None, 'Action7':None, 'Action8':None, 'Action9':None, 'Action10':None, 'Action11':None, 'Action12':None}, x, y)
    
    # render the UI to the screen
    def draw(self, dt=0):
        self.batch.draw()
        self.inventory.draw()
        
        if(self.cam is not None):
            self.cam.draw()