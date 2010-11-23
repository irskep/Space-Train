import pyglet, functools

import util, actionsequencer, interpolator

class DJ(object):
    """Spin phat beatz yo"""
    def __init__(self, handler, volume=1.0):
        super(DJ, self).__init__()
        self.handler = handler
        self.volume = volume
        
        self.player = pyglet.media.Player()
        self.player.eos_action = 'loop'
        self.player.volume = self.volume
        
        self.current_sound_name = ''
        self.next_sound_name = ''

        self.res = util.respath_func_with_base_path('music')
        
        self.sound_cache = {}

        self.seq = actionsequencer.ActionSequencer()
        self.interp = interpolator.InterpolatorController()
        
        self.update = self.interp.update_interpolators
    
    def get_sound(self, sound_name):
        # if not self.sound_cache.has_key(sound_name):
        #     self.sound_cache[sound_name] = pyglet.resource.media('music/%s.ogg' % sound_name, streaming=True)
        # return self.sound_cache[sound_name]
        return pyglet.resource.media('music/%s.ogg' % sound_name, streaming=True)
    
    def prime_cache(self, *args):
        # Make sure that things are cached so we don't get nasty delays later
        for arg in args:
            self.get_sound(arg)
    
    def transition_to(self, sound_name, fade=True):
        if fade:
            self.next_sound_name = sound_name
            self.fade_in(sound_name)
        else:
            new_sound = self.get_sound(sound_name)
            if self.current_sound_name == sound_name:
                fade_out = interpolator.LinearInterpolator(self.player, 'volume', 
                                                           start=0.0,
                                                           end=self.volume, name="volume", 
                                                           duration=3.0)
                self.interp.add_interpolator(fade_out)
            else:
                if not new_sound.is_queued:
                    self.player.queue(new_sound)
                if self.player.playing:
                    fade_out = interpolator.LinearInterpolator(self.player, 'volume', 
                                                               start=self.volume,
                                                               end=0.0, name="volume", duration=3.0,
                                                               done_function=self.next_track)
                    self.interp.add_interpolator(fade_out)
                else:
                    self.player.play()
    
    def fade_in(self, sound_name):
        new_sound = self.get_sound(sound_name)
        if not new_sound.is_queued:
            self.player.queue(new_sound)
        if self.player.playing:
            fade_out = interpolator.LinearInterpolator(self.player, 'volume', start=self.volume,
                                                        end=0.0, name="volume", duration=5.0,
                                                        done_function=self.fade_next_track)
            self.interp.add_interpolator(fade_out)
        else:
            self.player.volume = 0.0
            self.fade_next_track()
    
    def fade_next_track(self, dt=0):
        fade_in = interpolator.LinearInterpolator(self.player, 'volume', start=0.0,
                                                    end=self.volume, name="volume", duration=3.0)
        self.interp.add_interpolator(fade_in)
        self.player.play()
    
    def next_track(self, dt=0):
        self.current_sound_name = self.next_sound_name
        self.player.volume = 1.0
        self.player.next()
    
