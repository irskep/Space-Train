#r8xih7
import math, os, sys, json

import pyglet

from engine import gamestate
from editor import editorview

# pyglet.options['debug_gl'] = False

class AdventureMakerWindow(pyglet.window.Window):
    def __init__(self):
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        super(AdventureMakerWindow,self).__init__(width=screen.width-20, height=screen.height-80, vsync=True)
        gamestate.main_window = self
        gamestate.scripts_enabled = False
        gamestate.init_keys()
        
        with pyglet.resource.file(os.path.join('game', 'info.json'), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            self.set_caption("Adventure Maker: %s Edition" % game_info["name"])
            self.editorview = editorview.EditorView(sys.argv[1])
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
    
    def on_draw(self, dt=0):
        self.editorview.draw()
    
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
    

def run_game():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game', 'scenes'))
    main_window = AdventureMakerWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()