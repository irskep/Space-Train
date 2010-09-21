import os, sys, shutil, json, importlib, pyglet

import camera, actor, gamestate, settings, walkpath

import environment, scenehandler

class InterpolatorController(object):
    """Keeps track of the lifecycles of multiple interpolators"""
    def __init__(self):
        super(InterpolatorController, self).__init__()
        self.interpolators = set()
        
        # Shortcut to add a new interpolator
        self.add_interpolator = self.interpolators.add
    
    def update_interpolators(self, dt=0):
        to_remove = set()
        for i in self.interpolators:
            i.update(dt)
            if i.complete():
                to_remove.add(i)
        for i in to_remove:
            i.done_function(i)
        self.interpolators -= to_remove
        

class Scene(InterpolatorController):
    
    # Initialization
    def __init__(self, name):
        super(Scene, self).__init__()
        self.name = name
        self.batch = pyglet.graphics.Batch()
        self.actors = {}
        self.camera_points = {}
        
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            self.info = json.load(info_file)
        self.environment_name = self.info['environment']
        self.env = environment.Environment(self.environment_name)
        self.walkpath = walkpath.WalkPath(dict_repr = self.info['walkpath'])
        self.camera = camera.Camera(dict_repr=self.info['camera_points'])
        
        if gamestate.scripts_enabled:
            self.module = importlib.import_module(name)
            self.module.init(self, self.env)
            if self.module.myscene is None:
                self.module.myscene = self
        
        self.load_actors()
        
        if gamestate.scripts_enabled:
            self.module.scene_loaded()
    
    def resource_path(self, name):
        return '/'.join(['game', 'scenes', self.name, name])
    
    def load_actors(self):
        for identifier, attrs in self.info['actors'].viewitems():
            new_actor = actor.Actor(name=attrs['name'], identifier=identifier, scene=self)
            self.actors[identifier] = new_actor
            for attr in ['x', 'y', 'scale', 'rotation']:
                if attrs.has_key(attr):
                    setattr(new_actor.sprite, attr, attrs[attr])
            if attrs.has_key('walkpath_point'):
                new_actor.walkpath_point = attrs['walkpath_point']
                new_actor.sprite.position = self.walkpath.points[new_actor.walkpath_point]
    
    def dict_repr(self):
        self.info['actors'] = {i: act.dict_repr() for i, act in self.actors.viewitems()}
        self.info['walkpath'] = self.walkpath.dict_repr()
        self.info['camera_points'] = self.camera.dict_repr()
        return self.info
    
    def new_actor(self, actor_name, identifier=None, **kwargs):
        if identifier is None:
            next_identifier = 1
            while self.actors.has_key("%s_%d" % (actor_name, next_identifier)):
                next_identifier += 1
            identifier = "%s_%d" % (actor_name, next_identifier)
        new_actor = actor.Actor(identifier, actor_name, self, **kwargs)
        self.actors[identifier] = new_actor
        return new_actor
    
    def save_info(self):
        shutil.copyfile(self.resource_path('info.json'), self.resource_path('info.json~'))
        with pyglet.resource.file(self.resource_path('info.json'), 'w') as info_file:
            json.dump(self.dict_repr(), info_file, indent=4)
    
    
    # Events
    def fire_event(self, event, *args):
        self.module.handle_event(event, *args)
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.actors.has_key("main"):
            main = self.actors["main"]
            if main.prepare_move(*self.camera.mouse_to_canvas(x, y)):
                main.next_action()
    
    def actor_under_point(self, x, y):
        for act in self.actors.viewvalues():
            if act.covers_point(x, y):
                return act
    
    
    # Standard stuff
    def update(self, dt=0):
        self.camera.update(dt)
        self.update_interpolators(dt)
    
    @camera.obey_camera
    def draw(self, dt=0):
        self.env.draw()
        self.batch.draw()
        self.walkpath.draw()
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
