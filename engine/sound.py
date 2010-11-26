import pyglet

import util

class Sound(object):

    def __init__ (self, volume = 1.0):
        self.volume = volume

        self.player = pyglet.media.Player()
        self.player.volume = self.volume
        self.player.eos_action = 'stop'

        self.path = util.respath_func_with_base_path("sound")

        self.sound_cache = {}


    def get_sound(self, sound_name):
        if not self.sound_cache.has_key(sound_name):
            self.sound_cache[sound_name] = pyglet.resource.media('sound/%s.ogg' % sound_name,
                                                                 streaming=False)
        return self.sound_cache[sound_name]
    
    def play_sound(self, sound_name, volume = 1.0):
        self.get_sound(sound_name).play()
    
    
