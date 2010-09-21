import os, json, collections

import pyglet

import const, interpolator, util

class Actor(object):
    """Any non-static object that the player can interact with"""
    
    # All actor information is static, so it is stored in class variables.
    # Can be emptied upon exiting a scene, since different actors will likely be used.
    info = None
    images = None
    
    def __init__(self, identifier, name, scene, batch=None, x=0, y=0):
        self.name = name
        self.scene = scene
        self.actions = collections.deque()
        self.blocking_actions = 0
        self.identifier = identifier
        self.walkpath_point = None
        self.resource_path = util.respath_func_with_base_path('actors', self.name)
        
        self.update_static_info()
        self.current_state = Actor.info[self.name]['start_state']
        
        if self.scene and batch is None:
            batch = self.scene.batch
        self.sprite = pyglet.sprite.Sprite(Actor.images[self.name][self.current_state], 
                                           x=x, y=y, batch=batch)
    
    def __repr__(self):
        return 'Actor(name="%s", identifier=%s)' % (self.name, self.identifier)
    
    
    # Access
    
    def covers_point(self, x, y):
        min_x = self.sprite.x - self.sprite.image.anchor_x
        min_y = self.sprite.y - self.sprite.image.anchor_y
        max_x = self.sprite.x - self.sprite.image.anchor_x + self.sprite.image.width
        max_y = self.sprite.y - self.sprite.image.anchor_y + self.sprite.image.height
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    
    # State changes
    
    def set_image_if_exists(self, image_name):
        """Update image/animation if available, otherwise stay the same"""
        if Actor.images[self.name].has_key(image_name):
            self.sprite.image = Actor.images[self.name][image_name]
    
    def update_state(self, new_state, *args):
        """Update self.current_state and update animation if possible. Variable is
        changed even if animation is not changed so that scripts do not become confused."""
        self.current_state = new_state
        self.set_image_if_exists(new_state)
    
    
    # Action sequences
    
    def next_action(self, ending_action=None):
        """Completed one action, start another"""
        if self.blocking_actions > 0:
            self.blocking_actions -= 1
        if len(self.actions) > 0:
            action_list = self.actions.popleft()
            for action in action_list:
                self.blocking_actions += 1
                action[0](*action[1])   # I bet you are so confused as to what this does :-D
    
    
    # Possible actions to put in a sequence
    
    def move_to(self, pos, anim=None):
        interp = interpolator.Linear2DInterpolator(self.sprite, 'position', pos, speed=400.0, 
                                                   done_function=self.next_action)
        
        if anim and Actor.images[self.name].has_key(anim):
            self.update_state(anim)
        else:
            if pos[0] > self.sprite.x:
                self.update_state('walk_right')
            else:
                self.update_state('walk_left')
        self.scene.add_interpolator(interp)
    
    def fire_adv_event(self, event, *args):
        self.scene.fire_adv_event(event, *args)
        self.next_action()
    
    
    # Convenience methods for preparing standard action sequences
    
    def prepare_move(self, x, y):
        """Move toward (x, y) either straight or via walk path"""
        if self.blocking_actions == 0:
            if self.walkpath_point:
                self.prepare_walkpath_move(x, y)
            else:
                self.prepare_direct_move(x, y)
            return True
        return False
    
    def prepare_walkpath_move(self, x, y):
        wp = self.scene.walkpath;
        final_dest_point, moves = wp.move_sequence(self.walkpath_point, (x, y))
        if moves:
            for move in moves:
                # See move_to for what these args are
                self.actions.append([(self.move_to, move)])
            self.walkpath_point = final_dest_point
            info = {
                'actor': self,
                'point': self.walkpath_point
            }
            event_args = (const.WALK_PATH_COMPLETED, info)
            self.actions.append([
                (self.update_state, ['stand_front']),   # Stand still at the end
                (self.fire_adv_event, event_args)       # Send an event to the level script
            ])
    
    def prepare_direct_move(self, x, y):
        self.actions.append([(self.move_to, (x, y))])
        info = {
            'actor': self,
            'point': (x, y)
        }
        event_args = (const.WALK_COMPLETED, info)
        self.actions.append([
            (self.update_state, ['stand_front']),
            (self.fire_adv_event, event_args)
        ])
    
    
    # Serialization
    
    # No load_info() or save_info() because there is no graphical editor for Actors
    
    def update_static_info(self):
        """Initialize/update static Actor information"""
        if Actor.info == None or Actor.images == None:
            Actor.info = {}
            Actor.images = {}
        if not Actor.info.has_key(self.name) or not Actor.images.has_key(self.name):
            self.update_actor_info()
    
    def image_named(self, img_name, anchor_x, anchor_y):
        """Load and anchor a PNG"""
        img = pyglet.resource.image(self.resource_path("%s.png" % img_name))
        img.anchor_x = img.width * anchor_x
        img.anchor_y = img.height * anchor_y
        return img
    
    def update_actor_info(self):
        """Update static info for this Actor in particular"""
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            my_info = json.load(info_file)
            ax, ay = my_info['anchor_x'], my_info['anchor_y']
            Actor.info[self.name] = my_info
            Actor.images[self.name] = {}
            for state_name, num_frames in my_info['states'].viewitems():
                if num_frames == 1:
                    img = self.image_named(state_name, ax, ay)
                    Actor.images[self.name][state_name] = img
                else:
                    make_img = lambda i: self.image_named("%s_%d" % (state_name, i), ax, ay)
                    images = [make_img(i) for i in range(1, num_frames+1)]
                    # It may make sense to add this animation to its own texture bin later
                    anim = pyglet.image.Animation.from_image_sequence(images, 0.2);
                    Actor.images[self.name][state_name] = anim
    
    def dict_repr(self):
        """Store and return all information necessary to recreate this Actor's current state"""
        dict_repr = {'name': self.name}
        if self.walkpath_point:
            dict_repr['walkpath_point'] = self.walkpath_point
        else:
            dict_repr['x'] = int(self.sprite.x)
            dict_repr['y'] = int(self.sprite.y)
        return dict_repr
    

