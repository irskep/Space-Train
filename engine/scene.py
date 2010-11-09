"""
Controls all aspects of a single scene (background, overlay, and contained objects).

 ========================
 = Scene script methods =
 ========================

REQUIRED

handle_event(event_type, *args, **kwargs)
    event_type: see util.const
    args, kwargs: usually just a single dictionary 'info' is passed as a positional argument

OPTIONAL

init()
    Scene is finished loading, perform any necessary setup not done at the module level

transition_from(previous_scene)
    Called just before scene becomes visible after being switched to from previous_scene.
    Set character positions, etc.

actor_clicked(clicked_actor)
    clicked_actor was clicked by the user, do whatever or nothing

give_actor(receiving_actor, item)
    Return True if receiving_actor can/should receive item. Also start any event chains, 
    set variables, etc.
"""

import os, sys, shutil, json, importlib, pyglet, functools

import camera, actor, gamestate, util, interpolator, convo
from util import walkpath, zenforcer, pushmatrix

import cam, environment, gamehandler, scenehandler

update_t = 1/120.0

class ClipGroup(pyglet.graphics.OrderedGroup): 
    """Sprite group that clips to a rectangle"""
    def __init__(self, order=0, parent=None,
                 x=0, y=0, w=gamestate.norm_w, h=gamestate.norm_h):
        super(ClipGroup, self).__init__(order, parent)
        self.x, self.y, self.w, self.h = x, y, w, h
        # Some kind of weird ctypes issue here, need to re-cast
        self.x, self.y, self.w, self.h = [int(i) for i in (self.x, self.y, self.w, self.h)]
    
    def set_state(self):
        pyglet.gl.glScissor(int(self.x), int(self.y), int(self.w), int(self.h)) 
        pyglet.gl.glEnable(pyglet.gl.GL_SCISSOR_TEST) 
    
    def unset_state(self): 
        pyglet.gl.glDisable(pyglet.gl.GL_SCISSOR_TEST)
    

class Scene(object):
    
    # Initialization
    
    def __init__(self, name, scene_handler=None, ui=None, load_path=None, clip=True):
        super(Scene, self).__init__()
        self.name = name
        self.handler = scene_handler
        self.batch = pyglet.graphics.Batch()
        self.fresh = (load_path is None)
        if clip:
            self.main_group = ClipGroup(w=gamestate.main_window.width, 
                                        h=gamestate.main_window.height)
        else:
            self.main_group = None
        self.ui = ui
        self.actors = {}
        self.camera_points = {}
        self.interaction_enabled = True
        
        self.game_time = 0.0
        self.accum_time = 0.0
        self.clock = pyglet.clock.Clock(time_function=lambda: self.game_time)
        self.paused = False
        self.x_offset = 0.0
        self.y_offset = 0.0
        
        self.resource_path = util.respath_func_with_base_path('game', self.name)
        
        self.init_clock()
        self.init_zenforcer()
        self.interp = interpolator.InterpolatorController()
        self.convo = convo.Conversation(self)
        self.background_convos = set()
        self.init_convenience_bindings()
        
        self.load_info(load_path)
        self.initialize_from_info()
        self.load_actors()
        self.zenforcer.init_groups()
        
        if gamestate.scripts_enabled:
            self.load_script()
        
        self.update(0)
    
    def init_convenience_bindings(self):
        self.add_interpolator = self.interp.add_interpolator
    
    def init_zenforcer(self):
        def sprite_maker():
            for act in self.actors.viewvalues():
                yield act.sprite
        sort_func = lambda a, b: a.y < b.y
        self.zenforcer = zenforcer.ZEnforcer(self.main_group, sprite_maker, sort_func)
        pyglet.clock.schedule_interval(self.zenforcer.update, 1/30.0)
    
    def initialize_from_info(self):
        """Initialize objects specified in info.json"""
        self.environment_name = self.info['environment']
        self.env = environment.Environment(self.environment_name, self.main_group)
        self.walkpath = walkpath.WalkPath(dict_repr = self.info['walkpath'])
        self.camera = camera.Camera(dict_repr=self.info['camera_points'])
    
    def load_actors(self):
        """Initialize actors and update them with any values specified in the info dict"""
        for identifier, attrs in self.info['actors'].viewitems():
            # Initialize and store
            new_actor = actor.Actor(name=attrs['name'], identifier=identifier, 
                                    scene=self, attrs=attrs)
            
            # Obey walk paths
            if attrs.has_key('walkpath_point'):
                new_actor.walkpath_point = attrs['walkpath_point']
                new_actor.sprite.position = self.walkpath.points[new_actor.walkpath_point]
            self.add_actor(new_actor)
    
    def add_actor(self, actor):
        print "Adding actor %s" % actor.identifier
        self.actors[actor.identifier] = actor
        self.zenforcer.init_groups()
        self.zenforcer.update()
    
    def load_script(self):
        # Requires that game/scenes is in PYTHONPATH
        self.module = importlib.import_module(self.name)
        self.module.myscene = self
        self.call_if_available('init', self.fresh)
    
    
    # Cleanup
    
    def exit(self):
        for actor in self.actors.viewvalues():
            actor.sprite.delete()
        self.env.exit()
        pyglet.clock.unschedule(self.zenforcer.update)
    
    
    # Access
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
    def actor_under_point(self, x, y):
        possible_actors = {act for act in self.actors.viewvalues() if act.covers_point(x, y)}
        try:
            closest = possible_actors.pop()
            for act in possible_actors:
                if act.sprite.group > closest.sprite.group:
                    closest = act
            return closest
        except KeyError:
            return None
    
    
    # Script interaction
    
    def fire_adv_event(self, event, *args, **kwargs):
        if self.paused:
            return
        
        self.module.handle_event(event, *args, **kwargs)
    
    def call_if_available(self, func_name, *args, **kwargs):
        if hasattr(self.module, func_name):
            return getattr(self.module, func_name)(*args, **kwargs)
        else:
            return False
    
    def transition_from(self, old_scene_name):
        self.call_if_available('transition_from', old_scene_name)
    
    def begin_conversation(self, convo_name):
        self.convo.begin_conversation(convo_name)
    
    def begin_background_conversation(self, convo_name):
        new_convo = convo.Conversation(self, background=True)
        self.background_convos.add(new_convo)
        new_convo.begin_conversation(convo_name)
    
    def end_background_conversation(self, convo_name):
        to_remove = set()
        for c in self.background_convos:
            if c.convo_name == convo_name:
                to_remove.add(c)
        for c in to_remove:
            c.delete()
            self.background_convos.remove(c)
    
    def convo_in_progress(self):
        return self.convo.convo_name is not None
    
    
    # Events
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.paused:
            return
        if self.actors.has_key('main') and self.actors['main'].blocking_actions:
            return
        if self.convo_in_progress():
            return
        if not self.interaction_enabled:
            return
        
        clicked_actor = self.actor_under_point(*self.camera.mouse_to_canvas(x, y))
        
        if clicked_actor:
            self.click_actor(clicked_actor)
        elif self.actors.has_key("main"):
            self.move_main(x, y)
    
    def click_actor(self, clicked_actor):
        if(self.ui.inventory.held_item is not None):
            can_receive_item = self.call_if_available('give_actor', clicked_actor, 
                                                      self.ui.inventory.held_item)
            if not can_receive_item:
                self.ui.inventory.put_item(self.ui.inventory.held_item)
            self.ui.inventory.held_item = None
        else:
            self.call_if_available('actor_clicked', clicked_actor)
    
    def move_main(self, x, y):
        # Send main actor to click location according to actor's moving behavior
        main = self.actors["main"]
        while(main.blocking_actions > 0):
            main.next_action()
        dest_point = main.closest_valid_walkpath_point(*self.camera.mouse_to_canvas(x, y)):
        if hasattr(self.module, 'filter_move'):
            dest_point = self.module.filter_move(dest_point)
            if dest_point:
                main.prepare_walkpath_move(dest_point)
        else:
            main.prepare_walkpath_move(dest_point)
            main.next_action()
    
    def pause(self):
        self.paused = True
        print "%s is paused." % self.name
    
    def resume(self):
        self.paused = False
        print "%s has resumed." % self.name
    
    
    # Update/draw
    
    def update(self, dt=0):
        if self.paused: 
            return
        
        self.update_clock(dt)
        
        if self.actors.has_key('main'):
            self.camera.set_target(self.actors["main"].sprite.x, self.actors["main"].sprite.y,
                                   immediate=True)
        self.camera.update(dt)
        self.interp.update_interpolators(dt)
    
    def draw(self, dt=0):
        self.env.behind.blit(0,0,0)
        with camera.apply_camera(self.camera):
            if self.main_group:
                self.main_group.x = self.x_offset
                self.main_group.y = self.y_offset
            
            with pushmatrix(pyglet.gl.glTranslatef, self.x_offset, self.y_offset, 0):
                self.env.draw()
                self.batch.draw()
        
                self.env.draw_overlay()
                self.convo.draw()
                
                convos_to_remove = set()
                for c in self.background_convos:
                    c.draw()
                    if not c.active:
                        convos_to_remove.add(c)
                for c in convos_to_remove:
                    c.delete()
                    self.background_convos.remove(c)
    
    
    # Clock
    
    def init_clock(self):
        self.game_time = 0.0
        self.accum_time = 0.0
        self.clock = pyglet.clock.Clock(time_function=lambda: self.game_time)
    
    def update_clock(self, dt=0):
        # Align updates to fixed timestep 
        self.accum_time += dt 
        if self.accum_time > update_t * 3: 
            self.accum_time = update_t 
        while self.accum_time >= update_t: 
            self.game_time += update_t
            self.clock.tick() 
            self.accum_time -= update_t
    
    
    # Serialization
    
    def dict_repr(self):
        """Update and return all information necessary to recreate this Scene's current state"""
        self.info['actors'] = {i: act.dict_repr() for i, act in self.actors.viewitems()}
        self.info['walkpath'] = self.walkpath.dict_repr()
        self.info['camera_points'] = self.camera.dict_repr()
        return self.info
    
    def load_info(self, load_path=None):
        if load_path is None:
            with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
                self.info = json.load(info_file)
        else:
            self.info = util.load_json(load_path)
    
    def save_info(self):
        shutil.copyfile(self.resource_path('info.json'), self.resource_path('info.json~'))
        with pyglet.resource.file(self.resource_path('info.json'), 'w') as info_file:
            json.dump(self.dict_repr(), info_file, indent=4)
    
    
    # Editor methods
    
    def new_actor(self, actor_name, identifier=None, **kwargs):
        if identifier is None:
            next_identifier = 1
            while self.actors.has_key("%s_%d" % (actor_name, next_identifier)):
                next_identifier += 1
            identifier = "%s_%d" % (actor_name, next_identifier)
        new_actor = actor.Actor(identifier, actor_name, self, **kwargs)
        self.actors[identifier] = new_actor
        self.zenforcer.init_groups()
        return new_actor
    
    def remove_actor(self, identifier):
        self.actors[identifier].sprite.delete()
        del self.actors[identifier]
        self.zenforcer.init_groups()
    
    def load_song(self, song_name):
        self.song = pyglet.resource.media(song_name)
        song.play()
    
