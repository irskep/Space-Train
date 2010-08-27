#import cProfile
import pyglet, math, os

# pyglet.options['debug_gl'] = False

from pyglet import gl
from pyglet.window import key

from engine import env, settings

class AdventureWindow(pyglet.window.Window):
    def __init__(self):
        self.init_window()
        
        self.load_label = pyglet.text.Label(
            "Loading...", x=env.norm_w//2, y=env.norm_h//2,
            font_name='Gill Sans', font_size=48, anchor_x='center', anchor_y='center',
            color=(128,128,128,255)
        )
        
        fist_image = pyglet.resource.nested_image('characters', 'fist', 'stand_front.png')
        self.fist = pyglet.sprite.Sprite(fist_image, x=50, y=50)
        
        pyglet.clock.schedule(self.on_draw)
    
    def init_window(self):
        vsync = True
        
        if settings.fullscreen:
            super(AdventureWindow,self).__init__(fullscreen=True)
        else:
            super(AdventureWindow,self).__init__(width=env.norm_w, height=env.norm_h)
            self.set_caption("Space Train")
        
        env.main_window = self
        env.init_scale()
    
    def draw_load_screen(self):    
        gl.glClearColor(1,1,1,1)
        self.clear()
        self.load_label.draw()
    
    def on_draw(self, dt=0):
        env.dt = dt
        if env.scale_factor != 1.0:
            gl.glPushMatrix()
            env.scale()
        
        self.draw_load_screen()
        self.fist.draw()
        
        if env.scale_factor != 1.0:
            gl.glPopMatrix()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            return True
    

def run_game():
    main_window = AdventureWindow()
    pyglet.app.run()

if __name__ == '__main__':
    run_game()