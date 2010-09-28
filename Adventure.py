"""
Main file for the Space Train game engine. Run this.

-Add scene folder to PYTHONPATH so we can import scene scripts
-Open window and initialize game
-Start pyglet run loop
"""

import math, os, sys, json

# pyglet.options['debug_gl'] = False

import pyglet

from engine import gamestate, util
from engine import gamehandler

class AdventureWindow(pyglet.window.Window):
    """
    Basic customizations to Window, plus configuration.
    """
    def __init__(self, reset_save=False):
        if util.settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True, vsync=True)
        else:
            super(AdventureWindow,self).__init__(width=gamestate.norm_w, 
                                                 height=gamestate.norm_h, vsync=True)
        
        gamestate.main_window = self    # Make main window accessible to others.
                                        #   Necessary for convenient event juggling.
        gamestate.init_scale()          # Set up scaling transformations to have
                                        #   a consistent window size
        gamestate.init_keys()           # Set up some key event helpers
		
        # Load default game scene. Probably belongs in GameHandler actually.

        with pyglet.resource.file(util.respath('game', 'info.json'), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            game_info['reset_save'] = reset_save
            self.set_caption(game_info["name"])
            self.game_handler = gamehandler.GameHandler(**game_info)
        
        # gamestate.scaled is a decorator that wraps the given function in calls to
        # scale/unscale the OpenGL context. If/when AdventureWindow grows its own
        # on_draw() method, you can just write '@gamestate.scaled' above the function
        # definition.
        self.on_draw = self.game_handler.draw
        
        # Schedule drawing and update functions.
        # Draw really only needs 60 FPS, update can be faster.
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)

        
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
    
    def on_close(self):
        self.game_handler.prompt_save_and_quit()
    

def run_game():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game', 'scenes'))
    if len(sys.argv) == 2 and sys.argv[1] == 'newgame':
        main_window = AdventureWindow(True)
    else:
        main_window = AdventureWindow(False)
    pyglet.app.run()

if __name__ == '__main__':
    run_game()
