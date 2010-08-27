#import cProfile
import pyglet, math, os, sys

# pyglet.options['debug_gl'] = False

from pyglet import gl
from pyglet.window import key

from engine import state, settings
from engine import gamehandler

class AdventureWindow(pyglet.window.Window):
    def __init__(self):
        if settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True, vsync=True)
        else:
            super(AdventureWindow,self).__init__(width=state.norm_w, height=state.norm_h, vsync=True)
            self.set_caption("Space Train")
        
        state.main_window = self
        state.init_scale()
        self.game_handler = gamehandler.GameHandler(first_scene='test_initial')
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)
    
    def on_draw(self, dt=0):
        state.dt = dt
        if state.scale_factor != 1.0:
            gl.glPushMatrix()
            state.scale()
        
        self.game_handler.draw()
        
        if state.scale_factor != 1.0:
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