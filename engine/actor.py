import os, json, collections

import pyglet

import interpolator

def identifier_maker():
    next_identifier = 0
    while True:
        yield next_identifier
        next_identifier += 1

make_identifier = identifier_maker()

class Actor(object):
    
    info = None
    images = None
    
    def __init__(self, name, scene, identifier=None, batch=None, x=0, y=0):
        self.name = name
        self.scene = scene
        self.actions = collections.deque()
        self.blocking_actions = 0
        self.identifier = identifier or make_identifier.next()
        
        self.init_info()
        self.current_state = Actor.info[self.name]['start_state']
        self.sprite = pyglet.sprite.Sprite(Actor.images[self.name][self.current_state], 
                                           x=x, y=y, batch=batch)
    
    def init_info(self):
        if Actor.info == None or Actor.images == None:
            Actor.info = {}
            Actor.images = {}
        if not Actor.info.has_key(self.name) or not Actor.images.has_key(self.name):
            with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
                my_info = json.load(info_file)
                Actor.info[self.name] = my_info
                Actor.images[self.name] = {}
                for state_name, num_frames in my_info['states'].items():
                    if num_frames == 1:
                        img = pyglet.resource.image("%s.png" % self.resource_path(state_name))
                        img.anchor_x = img.width * my_info['anchor_x']
                        img.anchor_y = img.height * my_info['anchor_y']
                        Actor.images[self.name][state_name] = img
                    else:
                        images = []
                        for i in range(1, num_frames+1):
                            img = pyglet.resource.image("%s_%d.png" % (self.resource_path(state_name), i))
                            img.anchor_x = img.width * my_info['anchor_x']
                            img.anchor_y = img.height * my_info['anchor_y']
                            images.append(img)
                        bin = pyglet.image.atlas.TextureBin()
                        anim = pyglet.image.Animation.from_image_sequence(images, 0.2);
                        Actor.images[self.name][state_name] = anim
    
    def resource_path(self, name):
        return os.path.join('actors', self.name, name)
    
    def covers_point(self, x, y):
        min_x = self.sprite.x - self.sprite.image.anchor_x
        min_y = self.sprite.y - self.sprite.image.anchor_y
        max_x = self.sprite.x + self.sprite.image.anchor_x + self.sprite.image.width
        max_y = self.sprite.y + self.sprite.image.anchor_y + self.sprite.image.height
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def set_image_if_exists(self, image_name):
        if Actor.images[self.name].has_key(image_name):
            self.sprite.image = Actor.images[self.name][image_name]
    
    def update_state(self, new_state):
        self.current_state = new_state
        self.set_image_if_exists(new_state)
    
    def next_action(self):
        if len(self.actions) > 0:
            action_list = self.actions.popleft()
            for action in action_list:
                self.blocking_actions += 1
                action[0](*action[1])   # I bet you are so confused as to what this does :-D
    
    def handle_action_completed(self, action):
        self.blocking_actions -= 1
        if action.name == 'position':
            self.update_state('stand_front')
        self.next_action()
    
    def prepare_move(self, x, y):
        if self.blocking_actions == 0:
            # self.actions.append([(self.move_to, (x, y)), (self.demo_scaling, ())])
            self.actions.append([(self.move_to, (x, y))])
            self.next_action()
    
    def move_to(self, x, y):
        interp = interpolator.Linear2DInterpolator(self.sprite, 'position', (x,y), speed=400.0, 
                                                   done_function=self.handle_action_completed)
        if x > self.sprite.x:
            self.update_state('walk_right')
        else:
            self.update_state('walk_left')
        self.scene.add_interpolator(interp)
    
    def demo_scaling(self):
        interp = interpolator.LinearInterpolator(self.sprite, 'scale', start=0.0, end=1.0, duration=1.0, 
                                                   done_function=self.handle_action_completed)
        self.scene.add_interpolator(interp)
    
    def __repr__(self):
        return 'Character(name="%s", position=%s)' % (self.name, self.sprite.position)
    

