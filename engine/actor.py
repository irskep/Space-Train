import os, json, collections

import pyglet

import interpolator

class Actor(object):
    
    info = None
    images = None
    
    def __init__(self, name, scene, batch=None, x=0, y=0):
        self.name = name
        self.scene = scene
        self.actions = collections.deque()
        self.blocking_actions = 0
        
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
    
    def next_action(self):
        if len(self.actions) > 0:
            action_list = self.actions.popleft()
            for action in action_list:
                self.blocking_actions += 1
                action[0](*action[1])   # I bet you are so confused as to what this does :-D
    
    def handle_action_completed(self, action):
        self.blocking_actions -= 1
        self.next_action()
    
    def prepare_move(self, x, y):
        if self.blocking_actions == 0:
            self.actions.append([(self.move_to, (x, y)), (self.demo_scaling, ())])
            self.next_action()
    
    def move_to(self, x, y):
        interp = interpolator.Linear2DInterpolator(self.sprite, 'position', (x,y), speed=400.0, 
                                                   done_function=self.handle_action_completed)
        self.scene.add_interpolator(interp)
    
    def demo_scaling(self):
        interp = interpolator.LinearInterpolator(self.sprite, 'scale', start=0.0, end=1.0, duration=1.0, 
                                                   done_function=self.handle_action_completed)
        self.scene.add_interpolator(interp)
    
    def __repr__(self):
        return 'Character(name="%s", position=%s)>' % (self.name, self.sprite.position)
    

