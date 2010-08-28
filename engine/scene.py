import os, sys, json, importlib, pyglet

import actor, gamestate

import environment, scenehandler

class Scene(object):
    def __init__(self, name):
        self.name = name
        self.batch = pyglet.graphics.Batch()
        self.interpolators = set()
        self.actors = {}
        
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            self.info = json.load(info_file)
            self.environment_name = self.info['environment']
        
        self.env = environment.Environment(self.environment_name)
        
        if gamestate.scripts_enabled:
            self.module = importlib.import_module(name)
            self.module.init(self, self.env)
            if self.module.scene_handler is None:
                self.module.scene_handler = scenehandler.SceneHandler(self, self.env)
        
        self.load_actors()
        
        if gamestate.scripts_enabled:
            gamestate.main_window.push_handlers(self.module.scene_handler)
            self.module.scene_loaded()
    
    def resource_path(self, name):
        return os.path.join('game', 'scenes', self.name, name)
    
    def load_actors(self):
        for identifier, attrs in self.info['actors'].items():
            new_actor = actor.Actor(attrs['name'], scene=self, batch=self.batch)
            self.actors[identifier] = new_actor
            for attr in ['x', 'y', 'scale', 'rotation']:
                if attrs.has_key(attr):
                    setattr(new_actor.sprite, attr, attrs[attr])
    
    def add_interpolator(self, i):
        self.interpolators.add(i)
    
    def update(self, dt=0):
        gamestate.move_camera(dt)
        to_remove = set()
        for i in self.interpolators:
            i.update(dt)
            if i.complete():
                to_remove.add(i)
        for i in to_remove:
            i.done_function(i)
        self.interpolators -= to_remove
    
    def draw(self):
        gamestate.apply_camera()
        self.env.draw()
        self.batch.draw()
        gamestate.unapply_camera()
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
