"""
Handles game loading, saving, and initialization.
"""

import os, sys, json
import pyglet

import gamestate, util
import scene, scenehandler, ui

class GameHandler(object):
    """This class will be useful when scene transitions are implemented."""
    def __init__(self, first_scene, name="Adventure"):
        self.ui = ui.UI()
        
        self.name = name
        
        self.save_path = pyglet.resource.get_settings_path(self.name)
        util.mkdir_if_absent(self.save_path)
        
        self.scene_handler = scenehandler.SceneHandler(self)
        scn = self.load() or scene.Scene(first_scene, self.scene_handler, self.ui)
        self.scene_handler.set_first_scene(scn)
        self.update = self.scene_handler.update
    
    @gamestate.scaled
    def draw(self, dt=0):
        self.scene_handler.scene.draw()
        self.ui.draw()
        self.scene_handler.draw()
    
    # Called by scenehandler when the user is exiting the game, should prompt for a save
    def prompt_save_and_quit(self):
        self.save()
        pyglet.app.exit()
    
    # Serialization
    
    def dict_repr(self):
        return {
            'name': self.name,
            'first_scene': self.scene_handler.scene.name
        }
    
    def load(self, folder_name="autosave"):
        """Returns a scene if save existed and was loaded successfully"""
        base_path = os.path.join(self.save_path, folder_name)
        scn = self.scene_handler.scene
        if not os.path.exists(base_path):
            return None
        else:
            my_info = util.load_json(os.path.join(base_path, 'game'))
            return scene.Scene(my_info['first_scene'], self.scene_handler, self.ui,
                               load_path=os.path.join(base_path, my_info['first_scene']))
    
    def save(self, folder_name="autosave"):
        base_path = os.path.join(self.save_path, folder_name)
        print 'save to', base_path
        scn = self.scene_handler.scene
        util.mkdir_if_absent(base_path)
        util.save_json(self.dict_repr(), os.path.join(base_path, 'game'))
        util.save_json(scn.dict_repr(), os.path.join(base_path, scn.name))
    
