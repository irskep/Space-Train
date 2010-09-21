"""
Main file for the Space Train game engine. Run this.

-Add scene folder to PYTHONPATH so we can import scene scripts
-Open window and initialize game
-Start pyglet run loop
"""

import math, os, sys, json

# pyglet.options['debug_gl'] = False

import pyglet
from pyglet import gl

from engine import gamestate, settings
from engine import gamehandler

class AdventureWindow(pyglet.window.Window):
    """
    Basic customizations to Window, plus configuration.
    """
    def __init__(self):
        if settings.fullscreen:
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
        with pyglet.resource.file('/'.join(['game', 'info.json']), 'r') as game_info_file:
            game_info = json.load(game_info_file)
            self.set_caption(game_info["name"])
            self.game_handler = gamehandler.GameHandler(first_scene=game_info['first_scene'])
        
        # gamestate.scaled is a decorator that wraps the given function in calls to
        # scale/unscale the OpenGL context. If/when AdventureWindow grows its own
        # on_draw() method, you can just write '@gamestate.scaled' above the function
        # definition.
        self.on_draw = gamestate.scaled(self.game_handler.draw)
        
        # Schedule drawing and update functions.
        # Draw really only needs 60 FPS, update can be faster.
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)
    

    def on_draw(self, dt=0):
        if gamestate.scale_factor != 1.0:
            gl.glPushMatrix()
            gamestate.scale()
        
        self.game_handler.draw()
		
		#UI drawing here?
        
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