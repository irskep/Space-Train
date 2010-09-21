import json, pyglet

import gamestate, inventory, settings

class UI(object):
	
    # Initialization
    def __init__(self):
        self.cam = None
        self.batch = pyglet.graphics.Batch()
        self.sprites = []
        self.inventory = inventory.Inventory()
        img = pyglet.resource.nested_image('actors', 'fist', 'stand_front.png')
        img_data = img.get_image_data()
        img_w = img_data.width
        img_h = img_data.height
        sprite = pyglet.sprite.Sprite(img, x = gamestate.norm_w, y = gamestate.norm_h - img_h, batch=self.batch)
        self.sprites.append(sprite)
	
    # render the UI to the screen
    def draw(self):
        self.batch.draw()
        self.inventory.draw()