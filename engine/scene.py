import os, sys, json, importlib, pyglet

import game_state

import environment, scenehandler

class Scene(object):
    def __init__(self, name):
        self.name = name
        self.batch = pyglet.graphics.Batch()
        self.interpolators = set()
        
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            info = json.load(info_file)
            self.environment_name = info['environment']
        
        self.env = environment.Environment(self.environment_name)
        
        self.module = importlib.import_module(name)
        self.module.init(self, self.env)
        if self.module.scene_handler is None:
            self.module.scene_handler = scenehandler.SceneHandler(self, self.env)
        game_state.main_window.push_handlers(self.module.scene_handler)
    
    def resource_path(self, name):
        return os.path.join('game', 'scenes', self.name, name)
    
    def add_interpolator(self, i):
        print i
        self.interpolators.add(i)
    
    def update(self, dt=0):
        to_remove = set()
        for i in self.interpolators:
            i.update(dt)
            if i.complete():
                to_remove.add(i)
        self.interpolators -= to_remove
    
    def draw(self):
        self.env.draw()
        self.batch.draw()
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
