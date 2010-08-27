import os, json

import pyglet

import interpolator

class Actor(object):
    def __init__(self, name, batch=None, x=0, y=0):
        self.name = name
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            info = json.load(info_file)
            self.current_state = info['start_state']
            self.state_mappings = info['states']
        img = pyglet.resource.image("%s.png" % self.resource_path(self.current_state))
        self.sprite = pyglet.sprite.Sprite(img, x=x, y=y, batch=batch)
        self.draw = self.sprite.draw
    
    def resource_path(self, name):
        return os.path.join('actors', self.name, name)
    
    def move_to(self, x, y):
        interp = interpolator.PositionInterpolator(self.sprite, 'position', self.sprite.position, (x,y), speed=200.0)
        return interp
    
    def __repr__(self):
        return '<Character "%s" at (%d, %d)>' % (self.name, self.sprite.x, self.sprite.y)
    

