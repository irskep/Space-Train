import os, sys, shutil, json, importlib, pyglet

import actor, gamestate, settings

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
            new_actor = actor.Actor(name=attrs['name'], identifier=identifier, scene=self)
            self.actors[identifier] = new_actor
            for attr in ['x', 'y', 'scale', 'rotation']:
                if attrs.has_key(attr):
                    setattr(new_actor.sprite, attr, attrs[attr])
    
    def new_actor(self, actor_name, identifier=None, **kwargs):
        if identifier is None:
            next_identifier = 1
            while self.actors.has_key("%s_%d" % (actor_name, next_identifier)):
                next_identifier += 1
            identifier = "%s_%d" % (actor_name, next_identifier)
        new_actor = actor.Actor(identifier, actor_name, self, **kwargs)
        self.actors[identifier] = new_actor
        return new_actor
    
    def update_actor_info(self, act):
        if self.info['actors'].has_key(act.identifier):
            self.info['actors'][act.identifier]['x'] = act.sprite.x
            self.info['actors'][act.identifier]['y'] = act.sprite.y
        else:
            new_info = {
                'x': act.sprite.x,
                'y': act.sprite.y,
                'name': act.name
            }
            self.info['actors'][act.identifier] = new_info
        print self.info
    
    def save_info(self):
        shutil.copyfile(self.resource_path('info.json'), self.resource_path('info.json~'))
        
        with pyglet.resource.file(self.resource_path('info.json'), 'w') as info_file:
            json.dump(self.info, info_file, indent=4)
    
    def add_interpolator(self, i):
        self.interpolators.add(i)
    
    def actor_under_point(self, x, y):
        for act in self.actors.viewvalues():
            if act.covers_point(x, y):
                return act
    
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
    
