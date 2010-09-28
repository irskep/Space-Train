import os, sys, shutil, json, importlib, pyglet, functools

import camera, actor, gamestate, util, interpolator
from util import walkpath

import cam, environment, gamehandler, scenehandler


update_t = 1/60.0
class Scene(interpolator.InterpolatorController):
    
    # Initialization
    
    def __init__(self, name, scene_handler=None, ui=None, load_path=None):
        super(Scene, self).__init__()
        self.name = name
        self.handler = scene_handler
        self.batch = pyglet.graphics.Batch()
        self.ui = ui
        self.actors = {}
        self.camera_points = {}
        
        self.game_time = 0.0
        self.accum_time = 0.0
        self.clock = pyglet.clock.Clock(time_function=lambda: self.game_time) 
        self.paused = False
        self.convo_name = None
        self.convo_info = None
        self.convo_label = pyglet.text.Label("", color = (0,255,0,255), 
                                             font_size=12, anchor_x='center')
        
        self.resource_path = util.respath_func_with_base_path('game', self.name)
        
        self.load_info(load_path)
        self.initialize_from_info()
        self.load_actors()
        
        if gamestate.scripts_enabled:
            self.load_script()
    
    def initialize_from_info(self):
        """Initialize objects specified in info.json"""
        self.environment_name = self.info['environment']
        self.env = environment.Environment(self.environment_name)
        self.walkpath = walkpath.WalkPath(dict_repr = self.info['walkpath'])
        self.camera = camera.Camera(dict_repr=self.info['camera_points'])
    
    def load_actors(self):
        """Initialize actors and update them with any values specified in the info dict"""
        for identifier, attrs in self.info['actors'].viewitems():
            # Initialize and store
            new_actor = actor.Actor(name=attrs['name'], identifier=identifier, 
                                    scene=self, attrs=attrs)
            self.actors[identifier] = new_actor
            
            # Obey walk paths
            if attrs.has_key('walkpath_point'):
                new_actor.walkpath_point = attrs['walkpath_point']
                new_actor.sprite.position = self.walkpath.points[new_actor.walkpath_point]
    
    def load_script(self):
        # Requires that game/scenes is in PYTHONPATH
        self.module = importlib.import_module(self.name)
        self.module.myscene = self
        self.call_if_available('init')
        
    # Cleanup
    def exit(self):
        for actor in self.actors.viewvalues():
            actor.sprite.delete()
        self.env.exit()
    
    
    
    # Access
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
    def actor_under_point(self, x, y):
        return util.first(self.actors.viewvalues(), lambda act:act.covers_point(x, y))
    
    
    # Script interaction
    
    def fire_adv_event(self, event, *args):
        self.module.handle_event(event, *args)
    
    def call_if_available(self, func_name, *args, **kwargs):
        if hasattr(self.module, func_name):
            getattr(self.module, func_name)(*args, **kwargs)
    
    
    # Events
    
    def transition_from(self, old_scene_name):
        self.call_if_available('transition_from', old_scene_name)
    
    def on_mouse_release(self, x, y, button, modifiers):

        clicked_actor = self.actor_under_point(*self.camera.mouse_to_canvas(x, y))

        if clicked_actor:
            self.ui.actor_clicked(clicked_actor)
            self.call_if_available('actor_clicked', clicked_actor)
        elif self.actors.has_key("main"):
            # Send main actor to click location according to actor's moving behavior
            main = self.actors["main"]
            while(main.blocking_actions > 0):
                main.next_action()
            if main.prepare_move(*self.camera.mouse_to_canvas(x, y)):
                main.next_action()
    
    
    # Dialogue
    
    def begin_conversation(self, convo_name):
        # TODO: Instead of scheduling all at once, keep a convo line list
        # and schedule new one at end of old. Provides ability to skip by
        # clicking. Always a good thing.
        
        # Optimization: preload conversations in initializer
        self.convo_name = convo_name
        with pyglet.resource.file(self.resource_path("%s.convo" % convo_name), 'r') as f:
            self.convo_info = json.load(f)
        
        this_time = 0.0
        for line in self.convo_info['dialogue']:
            actor_id = line[0]
            text = line[1]
            # Maybe more options
            self.clock.schedule_once(functools.partial(self.speak, *line), this_time)
            this_time += max(len(text)*0.04, 2.0)
        self.clock.schedule_once(self.stop_speaking, this_time)
    
    def speak(self, actor_id, text, *args):
        if len(args) == 2:
            self.convo_info = args[0]
        for identifier, new_state in self.convo_info['at_rest'].viewitems():
            if identifier != actor_id:
                self.actors[identifier].update_state(new_state)
        act = self.actors[actor_id]
        act.update_state(self.convo_info['speaking'][actor_id])
        self.convo_label.begin_update()
        self.convo_label.x = act.sprite.x
        self.convo_label.y = act.sprite.y + 20 + \
                             act.current_image().height - act.current_image().anchor_y
        self.convo_label.text = text
        self.convo_label.end_update()
    
    def stop_speaking(self, dt=0):
        self.convo_label.begin_update()
        self.convo_label.text = ""
        self.convo_label.end_update()
        cn = self.convo_name
        self.convo_name = None  # Order matters here in case the script starts a new conversation
        self.convo_info = None
        self.call_if_available('end_conversation', cn)
    
    
    # Update/draw
    
    def update(self, dt=0):
        if self.paused: 
            return
        
        # Align updates to fixed timestep 
        self.accum_time += dt 
        if self.accum_time > update_t * 3: 
            self.accum_time = update_t 
        while self.accum_time >= update_t: 
            self.game_time += update_t
            self.clock.tick() 
            self.accum_time -= update_t
        
        if self.actors.has_key('main'):
            self.camera.set_target(self.actors["main"].sprite.x, self.actors["main"].sprite.y)
        self.camera.update(dt)
        self.update_interpolators(dt)
    
    @camera.obey_camera
    def draw(self, dt=0):
        self.env.draw()
        self.batch.draw()

        self.env.draw_overlay()
        self.convo_label.draw()

    
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
        return new_actor
    
    def remove_actor(self, identifier):
        self.actors[identifier].sprite.delete()
        del self.actors[identifier]
    
