import pyglet, os

from engine import gamestate

import draw

class Sidebar(object):
    def __init__(self):
        self.controls = []
        self.width = 100
        
        button_image = pyglet.resource.image(os.path.join('editor', 'widgets', 'imagebutton.png'))
        self.test_sprite = pyglet.sprite.Sprite(button_image, 0, 0)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.test_sprite.position = (x, y)
        self.draw()
        return pyglet.event.EVENT_HANDLED
    
    def draw(self):
        draw.set_color(0.8, 0.8, 0.8)
        draw.rect(0, 0, self.width, gamestate.main_window.height)
        for control in self.controls:
            control.draw()
        self.test_sprite.draw()
    
    def add(self, new_object):
        self.controls.append(new_object)
    
    def push_handlers(self):
        gamestate.main_window.push_handlers(self.controls)
        gamestate.main_window.push_handlers(self)
    
    def pop_handlers(self):
        gamestate.main_window.pop_handlers()
        gamestate.main_window.pop_handlers()
    

