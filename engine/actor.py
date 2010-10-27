import os, json, collections

import pyglet

import actionsequencer, interpolator, util

class Actor(actionsequencer.ActionSequencer):
    """Any non-static object that the player can interact with"""
    
    # All actor information is static, so it is stored in class variables.
    # Can be emptied upon exiting a scene, since different actors will likely be used.
    info = None
    images = None
    
    def __init__(self, identifier, name, scene, batch=None, attrs=None):
        super(Actor, self).__init__()
        attrs = attrs or None
        self.name = name
        self.scene = scene
        
        self.identifier = identifier
        self.walkpath_point = None
        self.resource_path = util.respath_func_with_base_path('actors', self.name)
        self.sound_path = util.respath_func_with_base_path('music')
        
        self.update_static_info()
        self.current_state = Actor.info[self.name]['start_state']
        
        if attrs.has_key('start_state'):
            self.current_state = attrs['start_state']
        
        if self.scene and batch is None:
            batch = self.scene.batch
        self.sprite = pyglet.sprite.Sprite(Actor.images[self.name][self.current_state], batch=batch)
        try:
            self.icon = pyglet.sprite.Sprite(self.image_named("icon", 0, 0), batch = None)
        except pyglet.resource.ResourceNotFoundException:
            self.icon = pyglet.sprite.Sprite(Actor.images[self.name][self.current_state], batch = None) 
            if self.scene.ui:
                if self.icon.height > self.scene.ui.inventory.height:
                    self.icon.scale = float(self.scene.ui.inventory.height) / float(self.icon.height)
        
        # Update attributes
        for attr in ['x', 'y', 'scale', 'rotation']:
            if attrs.has_key(attr):
                setattr(self.sprite, attr, attrs[attr])
        
        self.anchor_x = Actor.info[self.name]['anchor_x']
        self.anchor_y = Actor.info[self.name]['anchor_y']
    
    def __repr__(self):
        return 'Actor(name="%s", identifier=%s)' % (self.name, self.identifier)
    
    
    # Access
    
    def covers_point(self, x, y):
        if not self.sprite.visible:
            return False
        min_x = self.abs_position_x()
        min_y = self.abs_position_y()
        max_x = self.abs_position_x() + self.width()
        max_y = self.abs_position_y() + self.height()
        return min_x <= x <= max_x and min_y <= y <= max_y
        
    def icon_covers_point(self, x, y):
        min_x = self.icon.x - self.icon.image.anchor_x
        min_y = self.icon.y - self.icon.image.anchor_y
        max_x = self.icon.x - self.icon.image.anchor_x + self.icon.width*self.icon.scale
        max_y = self.icon.y - self.icon.image.anchor_y + self.icon.height*self.icon.scale
        return min_x <= x <= max_x and min_y <= y <= max_y
            
    def covers_visible_point(self, x, y):
        min_x = self.abs_position_x()
        min_y = self.abs_position_y()
        max_x = self.abs_position_x() + self.width()
        max_y = self.abs_position_y() + self.height()
        if min_x <= x <= max_x and min_y <= y <= max_y:
            return (util.image_alpha_at_point(self.current_image(),  x-min_x, y-min_y))
    
    # Convenience methods to tell the position, width, and height of the actor
    def width(self):
        return self.current_image().width*self.sprite.scale
    
    def height(self):
        return self.current_image().height*self.sprite.scale
    
    def abs_position_x(self):
        return self.sprite.x - self.current_image().anchor_x
    
    def abs_position_y(self):
        return self.sprite.y - self.current_image().anchor_y
    
    def current_image(self):
        try:
            return self.sprite.image.frames[0].image
        except AttributeError:
            return self.sprite.image
    
    # State changes
    
    def set_image_if_exists(self, image_name):
        """Update image/animation if available, otherwise stay the same"""
        if Actor.images[self.name].has_key(image_name):
            self.sprite.image = Actor.images[self.name][image_name]
    
    def update_state(self, new_state):
        """Update self.current_state and update animation if possible. Variable is
        changed even if animation is not changed so that scripts do not become confused."""
        if new_state != self.current_state:
            self.current_state = new_state
            self.set_image_if_exists(new_state)
    
    # Possible actions to put in a sequence. Pay attention for parameter values.
    
    def move_to(self, pos, anim=None):
        """Set up an interpolator to move between this actor's current position and
        the given position, choosing a walk animation automatically if non is provided"""
        InterpClass = interpolator.Linear2DInterpolator # Gee golly this name is long
        interp = InterpClass(self.sprite, 'position', pos, speed=400.0, 
                             done_function=self.next_action)
        
        if not anim or not Actor.images[self.name].has_key(anim):
            if pos[0] < self.sprite.x:
                anim = 'walk_left'
            else:
                anim = 'walk_right'
        self.update_state(anim)
        self.scene.add_interpolator(interp)
    
    def jump(self):
        InterpClass = interpolator.JumpInterpolator # Gee golly this name is long
        interp = InterpClass(self.sprite, 'y', 100, duration=0.3, done_function=self.next_action)
        self.update_state('jump')
        self.scene.add_interpolator(interp)
    
    def fire_adv_event(self, event, *args):
        self.scene.fire_adv_event(event, *args)
        self.next_action()
    
    
    
    # Convenience methods for preparing standard action sequences
    
    def prepare_move(self, x, y):
        """Move toward (x, y) either straight or via walk path"""
        if self.blocking_actions == 0:
            if self.walkpath_point:
                # Find the closest reachable walkpath point
                ok = False
                excluded_points = set()
                dest_point = self.scene.walkpath.point_near(x, y, exclude=excluded_points)
                while not ok:
                    try:
                        self.prepare_walkpath_move(dest_point)
                        ok = True
                    except IndexError:
                        # dijkstra.py throws IndexError if no path exists
                        # (internal heap gets over-popped)
                        excluded_points.add(dest_point)
                        dest_point = self.scene.walkpath.point_near(x, y, exclude=excluded_points)
            else:
                self.prepare_direct_move(x, y)
            return True
        else:
            return False
    
    def prepare_walkpath_move(self, dest_point):
        wp = self.scene.walkpath
        final_dest_point, moves = wp.move_sequence_between(self.walkpath_point, dest_point)
        if moves:
            for move in moves:
                # See move_to for what these args are
                self.actions.append([(self.move_to, move)])
            self.walkpath_point = final_dest_point
            info = {
                'actor': self,
                'point': self.walkpath_point
            }
            event_args = (util.const.WALK_PATH_COMPLETED, info)
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
        event_args = (util.const.WALK_COMPLETED, info)
        self.actions.append([
            (self.update_state, ['stand_front']),
            (self.fire_adv_event, event_args)
        ])
    
    def prepare_jump(self):
        self.actions.append([(self.jump, [])])
        self.actions.append([(self.update_state, ['stand_front'])])
    
    
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
            for state_name, state_info in my_info['states'].viewitems():
                if isinstance(state_info, list):
                    num_frames = state_info[0]
                    time_per_frame = state_info[1]
                else:
                    num_frames = state_info
                    time_per_frame = 0.2
                if num_frames == 1:
                    img = self.image_named(state_name, ax, ay)
                    Actor.images[self.name][state_name] = img
                else:
                    make_img = lambda i: self.image_named("%s_%d" % (state_name, i), ax, ay)
                    images = [make_img(i) for i in range(1, num_frames+1)]
                    # It may make sense to add this animation to its own texture bin later
                    anim = pyglet.image.Animation.from_image_sequence(images, time_per_frame);
                    Actor.images[self.name][state_name] = anim
    
    def dict_repr(self):
        """Store and return all information necessary to recreate this Actor's current state"""
        dict_repr = {'name': self.name}
        if self.walkpath_point:
            dict_repr['walkpath_point'] = self.walkpath_point
        else:
            dict_repr['x'] = int(self.sprite.x)
            dict_repr['y'] = int(self.sprite.y)
        dict_repr['start_state'] = self.current_state
        if self.sprite.scale != 1.0:
            dict_repr['scale'] = self.sprite.scale
        return dict_repr

    def play_sound(self, load_sound):
        self.sound = pyglet.resource.media(self.sound_path("%s.mp3" % load_sound))
        self.sound.play()


    
