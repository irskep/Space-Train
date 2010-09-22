import sys
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
        self.cam = cam.CAM({'Action': lambda: sys.stdout.write("Action pressed\n"), 'Action2': lambda: sys.stdout.write("Action2 pressed\n"), 
                            'Action3': lambda: sys.stdout.write("Action3 pressed\n"), 'Action4': lambda: sys.stdout.write("Action4 pressed\n"), 'Action5': lambda: sys.stdout.write("Action5 pressed\n")}, 
                            x, y, 90)
        return True
    
    # render the UI to the screen
    def draw(self):
        self.batch.draw()
        self.inventory.draw()
        
        if(self.cam is not None):
            self.cam.draw()