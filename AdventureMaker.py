import math, os, sys, json

import pyglet

import engine
from engine import gamestate, util
from editor import editorview

# pyglet.options['debug_gl'] = False
pyglet.options['graphics_vbo'] = False

class AdventureMakerWindow(pyglet.window.Window):
    def __init__(self):
        if len(sys.argv) < 2:
            print "Usage: python AdventureMaker.py <name of scene to edit>"
            sys.exit(1)
        
        screen = pyglet.window.get_platform().get_default_display().get_default_screen()
        super(AdventureMakerWindow,self).__init__(width=screen.width-20, 
                                                  height=gamestate.norm_h, 
                                                  vsync=True)
        gamestate.main_window = self
        gamestate.scripts_enabled = False
        gamestate.init_scale()
        gamestate.keys = pyglet.window.key.KeyStateHandler()
        gamestate.main_window.push_handlers(gamestate.keys)
        
        engine.init()
        
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        
        self.set_caption("Scene Editor: %s" % sys.argv[1])
        self.editorview = editorview.EditorView(sys.argv[1])
        
        pyglet.clock.schedule_interval(self.on_draw, 1/60.0)
        pyglet.clock.schedule_interval(self.editorview.update, 1/120.0)
    
    def on_draw(self, dt=0):
        self.editorview.draw()
    
    def on_key_press(self, symbol, modifiers):
        # Override default behavior of escape key quitting
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED
    

def run_game():
    sys.path.append('/'.join([os.path.dirname(__file__), 'game']))
    main_window = AdventureMakerWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()