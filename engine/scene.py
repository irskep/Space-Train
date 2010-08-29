import os, sys, shutil, json, importlib, pyglet

import camera, actor, gamestate, settings, walkpath

import environment, scenehandler

class Scene(object):
    def __init__(self, name):
        self.name = name
        self.batch = pyglet.graphics.Batch()
        self.interpolators = set()
        self.actors = {}
        self.camera_points = {}
        
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            self.info = json.load(info_file)
        self.environment_name = self.info['environment']
        self.env = environment.Environment(self.environment_name)
        self.walkpath = walkpath.WalkPath(dict_repr = self.info['walkpath'])
        self.camera = camera.Camera(points_dict=self.info['camera_points'])
        
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
        for identifier, attrs in self.info['actors'].viewitems():
            new_actor = actor.Actor(name=attrs['name'], identifier=identifier, scene=self)
            self.actors[identifier] = new_actor
            for attr in ['x', 'y', 'scale', 'rotation']:
                if attrs.has_key(attr):
                    setattr(new_actor.sprite, attr, attrs[attr])
            if attrs.has_key('walkpath_point'):
                new_actor.walkpath_point = attrs['walkpath_point']
                new_actor.position = self.walkpath.points[new_actor.walkpath_point]
    
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
        if act is None:
            return
        if self.info['actors'].has_key(act.identifier):
            self.info['actors'][act.identifier]['x'] = int(act.sprite.x)
            self.info['actors'][act.identifier]['y'] = int(act.sprite.y)
        else:
            new_info = {
                'x': int(act.sprite.x),
                'y': int(act.sprite.y),
                'name': act.name
            }
            self.info['actors'][act.identifier] = new_info
    
    def save_info(self):
        shutil.copyfile(self.resource_path('info.json'), self.resource_path('info.json~'))
        self.info['walkpath'] = self.walkpath.dict_repr()
        self.info['camera_points'] = self.camera.points_dict()
        with pyglet.resource.file(self.resource_path('info.json'), 'w') as info_file:
            json.dump(self.info, info_file, indent=4)
    
    def add_interpolator(self, i):
        self.interpolators.add(i)
    
    def actor_under_point(self, x, y):
        for act in self.actors.viewvalues():
            if act.covers_point(x, y):
                return act
    
    def update(self, dt=0):
        self.camera.update(dt)
        to_remove = set()
        for i in self.interpolators:
            i.update(dt)
            if i.complete():
                to_remove.add(i)
        for i in to_remove:
            i.done_function(i)
        self.interpolators -= to_remove
    
    def draw(self):
        self.camera.apply()
        self.env.draw()
        self.batch.draw()
        self.camera.unapply()
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
