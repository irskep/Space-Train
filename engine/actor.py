import os, json

import pyglet

import interpolator

class Actor(object):
    
    info = None
    images = None
    
    def __init__(self, name, batch=None, x=0, y=0):
        self.name = name
        if Actor.info == None:
            with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
                Actor.info = json.load(info_file)
                Actor.images = {}
                for state_name, num_frames in Actor.info['states'].items():
                    dict_name = "%s.%s" % (name, state_name)
                    if num_frames == 1:
                        img = pyglet.resource.image("%s.png" % self.resource_path(state_name))
                        Actor.images[dict_name] = img
                    else:
                        images = []
                        for i in range(1, num_frames+1):
                            img = pyglet.resource.image("%s_%d.png" % (self.resource_path(state_name), i))
                            images.append(img)
                        bin = pyglet.image.atlas.TextureBin()
                        anim = pyglet.image.Animation.from_image_sequence(images, 0.2);
                        Actor.images[dict_name] = anim
        self.current_state = Actor.info['start_state']
        self.sprite = pyglet.sprite.Sprite(Actor.images["%s.%s" % (self.name, self.current_state)], 
                                           x=x, y=y, batch=batch)
        self.draw = self.sprite.draw
    
    def resource_path(self, name):
        return os.path.join('actors', self.name, name)
    
    def move_to(self, x, y):
        interp = interpolator.Linear2DInterpolator(self.sprite, 'position', (x,y), speed=400.0)
        return interp
    
    def __repr__(self):
        return '<Character "%s" at (%d, %d)>' % (self.name, self.sprite.x, self.sprite.y)
    

