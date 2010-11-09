"""
Main file for the Space Train game engine. Run this.

-Add scene folder to PYTHONPATH so we can import scene scripts
-Open window and initialize game
-Start pyglet run loop
"""

import math, os, sys, json

# pyglet.options['debug_gl'] = False

import pyglet

import engine
from engine import gamestate, util
from engine import gamehandler, eventmanager

class AdventureWindow(pyglet.window.Window):
    """
    Basic customizations to Window, plus configuration.
    """
    def __init__(self, reset_save=False, reset_at_scene=None):
        reset_save = reset_save or reset_at_scene
        if util.settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True, vsync=True)
        else:
            super(AdventureWindow,self).__init__(width=gamestate.norm_w, 
                                                 height=gamestate.norm_h, vsync=True)
        
        gamestate.main_window = self    # Make main window accessible to others.
                                        #   Necessary for convenient event juggling.
        gamestate.init_scale()          # Set up scaling transformations to have
                                        #   a consistent window size
        gamestate.event_manager = eventmanager.EventManager()
        
        self.game_handler = None
        
        engine.init()                   # Set up resource paths
        
        self.load_fraction = 0.0

        with pyglet.resource.file(util.respath('game', 'info.json'), 'r') as game_info_file:
            self.game_info = json.load(game_info_file)
            self.game_info['reset_save'] = reset_save
            if reset_at_scene:
                self.game_info['first_scene'] = reset_at_scene
            self.set_caption(self.game_info["name"])
        
        # Stupid hack to get around pyglet loading bullshit
        pyglet.clock.schedule_once(self.finish_loading, 0.0000001)
    
    def finish_loading(self, dt=0):
        self.preload()
        self.game_handler = gamehandler.GameHandler(**self.game_info)
        
        # Schedule drawing and update functions.
        # Draw really only needs 60 FPS, update can be faster.
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.game_handler.update, 1/120.0)
    
    def preload(self):
        self.on_draw()
        self.flip()
        i = 0
        for item in util.preload:
            try:
                util.load_image(item)
            except pyglet.resource.ResourceNotFoundException:
                print "bad", item
            i += 1
            self.load_fraction = float(i)/float(len(util.preload))
            self.on_draw()
            self.flip()
            # pyglet.app.event_loop.idle()

    def on_draw(self, dt=0):
        if self.game_handler:
            self.game_handler.draw()
        else:
            util.draw.set_color(0,0,0)
            util.draw.rect(0,0,self.width,self.height)
            util.draw.set_color(0,255,0)
            util.draw.rect(0, self.height/2-20, self.width*self.load_fraction, self.height/2+20)
    
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
    
    def on_close(self):
        self.game_handler.prompt_save_and_quit()
    

def run_game():
    sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))
    if len(sys.argv) == 2:
        if sys.argv[1] == 'newgame':
            main_window = AdventureWindow(True)
        else:
            main_window = AdventureWindow(True, sys.argv[1])
    else:
        main_window = AdventureWindow(False)
    pyglet.app.run()

if __name__ == '__main__':
    run_game()
