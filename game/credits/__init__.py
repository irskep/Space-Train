import pyglet
import functools

from engine import actor
from engine.interpolator import FadeInterpolator, LinearInterpolator, Random2DInterpolator
from engine.gamestate import norm_w, norm_h


# myscene is set by scene.py
myscene = None

# wait_time = lambda text: max(len(text)*0.015, 3.0)+3.0
wait_time = lambda text: 3.0

note_actor = None
can_continue = False

def init(fresh=True):
    myscene.interaction_enabled = False
    myscene.moving_camera = True
    # I'M A GIANT CHEATER
    myscene.camera.constrain_point = lambda x, y: (x, y)
    
    myscene.ui.inventory.visible = False
    billboard = myscene.new_actor('a_train_in_spain', 'billboard', attrs=dict(x=640, y=360))
    billboard.update_state('explode_1')
    
    def show_n(n):
        def show(dt=0):
            billboard.update_state('explode_%d' % n)
        return show
    
    for t in xrange(1, 4):
        pyglet.clock.schedule_once(show_n(t+1), 3.0*t)
    
    def shakeshakeshake(dt=0):
        myscene.play_sound('space_train_explode')
        interp = Random2DInterpolator(myscene.camera, 'position', 20.0, duration=9.0)
        myscene.add_interpolator(interp)
    
    pyglet.clock.schedule_once(shakeshakeshake, 3.0)
    

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
    global can_continue
    can_continue = True
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
    if clicked_actor.identifier == "note" and can_continue:
        myscene.fade_music(0.95)
        myscene.handler.notify("act1_scene1")
