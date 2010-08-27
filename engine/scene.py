import os, sys, json, importlib, pyglet

import game_state

import environment

class Scene(object):
    def __init__(self, name):
        self.name = name
        self.batch = pyglet.graphics.Batch()
        with pyglet.resource.file(self.resource_path('info.json'), 'r') as info_file:
            info = json.load(info_file)
            self.environment_name = info['environment']
            self.env = environment.Environment(self.environment_name)
            self.draw = self.env.draw
        self.module = importlib.import_module(name)
        self.module.init(self, self.env)
        game_state.main_window.push_handlers(self.module.scene_handler)
    
    def resource_path(self, name):
        return os.path.join('game', 'scenes', self.name, name)
    
    def update(self, dt=0):
        pass
    
    def __repr__(self):
        return 'Scene(name="%s")' % self.name
    
