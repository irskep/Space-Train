import pyglet
import functools

from engine import actor
from engine.interpolator import FadeInterpolator, LinearInterpolator
from engine.gamestate import norm_w, norm_h


# myscene is set by scene.py
myscene = None

# wait_time = lambda text: max(len(text)*0.015, 3.0)+3.0
wait_time = lambda text: 3.0

note_actor = None

def init(fresh=True):
    global note_actor
    note_actor = myscene.new_actor('intro_billboards', 'note', attrs=dict(x=640, y=360, opacity=0))
    
    myscene.play_music('intro', fade=False)
    pyglet.clock.schedule_once(begin, 2.0)
    
    # t = show_sequence(sequence)
    myscene.ui.inventory.visible = False

def transition_from(old_scene):
    pass
    
def begin(dt=0):
    q1 = "The only way of catching a train I have ever discovered is to miss the train before.\n" +\
         "- Gilbert K. Chesterton (1874-1936)"
    q2 = "I knew I was going to take the wrong train, so I left early.\n" + \
         "--Yogi Berra (1925-2014)"
    t = spawn_text(q1, 0.045, 0.45, 0.75)
    
    pyglet.clock.schedule_once(functools.partial(spawn_text, q2, 0.045, 0.55, 0.25), 4.0)
    
    pyglet.clock.schedule_once(show_letter, t+7.0)

def show_letter(dt=0):
    interp = LinearInterpolator(note_actor.sprite, 'opacity', start=0, end=255, name="fade", duration=3.0)
    myscene.interp.add_interpolator(interp)    

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
        myscene.fade_music(1.0)
        pyglet.clock.schedule_once(next, 1.1)

def next(dt=0):
    myscene.handler.notify("act1_scene1")
