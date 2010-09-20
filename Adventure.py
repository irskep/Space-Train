import math, os, sys, json

# pyglet.options['debug_gl'] = False

import pyglet
from pyglet import gl

from engine import gamestate, settings
from engine import gamehandler

class AdventureWindow(pyglet.window.Window):
    def __init__(self):
        if settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True, vsync=True)
        else:
            super(AdventureWindow,self).__init__(width=gamestate.norm_w, 
                                                 height=gamestate.norm_h, vsync=True)
        
        gamestate.main_window = self
        gamestate.init_scale()
        gamestate.init_keys()
		
        with pyglet.resource.file('/'.join(['game', 'info.json']), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            self.set_caption(game_info["name"])
            self.game_handler = gamehandler.GameHandler(first_scene=game_info['first_scene'])
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)
    
    def on_draw(self, dt=0):
        if gamestate.scale_factor != 1.0:
            gl.glPushMatrix()
            gamestate.scale()
        
        self.game_handler.draw()
        
        if gamestate.scale_factor != 1.0:
            gl.glPopMatrix()
    
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
    

def run_game():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game', 'scenes'))
    main_window = AdventureWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()