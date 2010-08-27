#r8xih7
import pyglet, math, os, sys, json

# pyglet.options['debug_gl'] = False

from pyglet import gl
from pyglet.window import key

from engine import game_state, settings
from engine import gamehandler

class AdventureWindow(pyglet.window.Window):
    def __init__(self):
        if settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True, vsync=True)
        else:
            super(AdventureWindow,self).__init__(width=game_state.norm_w, height=game_state.norm_h, vsync=True)
            self.set_caption("Space Train")
        
        game_state.main_window = self
        game_state.init_scale()
        
        with pyglet.resource.file(os.path.join('game', 'info.json'), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            self.game_handler = gamehandler.GameHandler(first_scene=game_info['first_scene'])
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)
    
    def on_draw(self, dt=0):
        game_state.dt = dt
        if game_state.scale_factor != 1.0:
            gl.glPushMatrix()
            game_state.scale()
        
        self.game_handler.draw()
        
        if game_state.scale_factor != 1.0:
            gl.glPopMatrix()
    
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == key.ESCAPE:
            return True
    

def run_game():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game', 'scenes'))
    main_window = AdventureWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()