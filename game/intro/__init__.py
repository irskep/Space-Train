import pyglet
import functools

from engine import actor
from engine.interpolator import FadeInterpolator, LinearInterpolator
from engine.gamestate import norm_w, norm_h


# myscene is set by scene.py
myscene = None

# wait_time = lambda text: max(len(text)*0.015, 3.0)+3.0
wait_time = lambda text: 1.0

def init(fresh=True):
    pyglet.clock.schedule_once(begin, 2.0)
    
    # t = show_sequence(sequence)
    myscene.ui.inventory.visible = False

def transition_from(old_scene):
    pass
    
def begin(dt=0):
    t = spawn_text("I knew I was going to take the wrong train, so I left early.\n" + 
                   "--Yogi Berra (1925-2014)", 0.05, 0.5, 0.75)
    
    pyglet.clock.schedule_once(show_letter, t+2.0)

def show_letter(dt=0):
    new_actor = myscene.new_actor('intro_billboards', 'note', attrs=dict(x=640, y=360, opacity=0))
    
    def fade_in():
        interp = LinearInterpolator(new_actor.sprite, 'opacity', start=0, end=255, name="fade", duration=3.0)
        myscene.interp.add_interpolator(interp)
    
    def fade_out(dt=0):
        interp = LinearInterpolator(new_actor.sprite, 'opacity', start=255, end=0, name="fade", duration=3.0)
        myscene.interp.add_interpolator(interp)
    
    fade_in()

def show_sequence(sequence=(), t=2.0):
    for args in sequence:
        pyglet.clock.schedule_once(functools.partial(spawn_text, *args), t)
        t += wait_time(args[0])
    pyglet.clock.schedule_once(end_sequence, t)
    return t

def end_sequence(dt=0):
    myscene.handler.notify('act1_scene1')

def spawn_text(text, size, x, y, dt=0):
    l = pyglet.text.Label(text, font_name=['Verdana', 'Helvetica'], font_size=norm_h*size, 
                          anchor_x='center', anchor_y='center', batch=myscene.batch,
                          color=(255, 255, 255, 255), x=norm_w*x, y=norm_h*y)
    if l.content_width > 960:
        l.delete()
        l = pyglet.text.Label(text, font_name=['Courier', 'Helvetica'], font_size=norm_h*size, 
                              anchor_x='center', anchor_y='center', batch=myscene.batch,
                              color=(255, 255, 255, 255), x=norm_w*x, y=norm_h*y,
                              multiline=True, width=960)
    def start_text():
        interp = FadeInterpolator(l, 'color', start=0, end=255, name="fade", duration=2.0)
        myscene.interp.add_interpolator(interp)
    
    def end_text(dt=0):
        interp = FadeInterpolator(l, 'color', start=255, end=0, name="fade", duration=2.0)
        myscene.interp.add_interpolator(interp)
    
    start_text()
    pyglet.clock.schedule_once(end_text, wait_time(text)+3.0)
    return wait_time(text)+3

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    if clicked_actor.identifier == "note":
        myscene.handler.notify("act1_scene1")
