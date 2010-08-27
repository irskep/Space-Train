import os, sys, json, importlib

import settings

import environment

class Scene(object):
    def __init__(self, name):
        self.name = name
        self.path = os.path.join('game', 'scenes', name)
        with open(os.path.join(self.path, 'info.json'), 'r') as info_file:
            info = json.load(info_file)
            self.environment_name = info['environment']
            self.env = environment.Environment(self.environment_name)
        self.module = importlib.import_module(name)
        self.module.init(self.env)
    
    def update(self, dt=0):
        pass
    
