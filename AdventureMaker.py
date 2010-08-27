#r8xih7
import pyglet, math, os, sys, json

# pyglet.options['debug_gl'] = False

from pyglet import gl
from pyglet.window import key

from engine import game_state, settings
from engine import gamehandler

class AdventureMakerWindow(pyglet.window.Window):
    def __init__(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        super(AdventureMakerWindow,self).__init__(width=screen.width-20, height=screen.height-80, vsync=True)
        game_state.scripts_enabled = False
        
        with pyglet.resource.file(os.path.join('game', 'info.json'), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            self.set_caption("Adventure Maker: %s Edition" % game_info["name"])
            self.game_handler = gamehandler.GameHandler(first_scene=game_info['first_scene'])
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
    
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
    main_window = AdventureMakerWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()