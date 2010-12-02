import pyglet
import functools
import yaml
import random

from engine import actor
from engine.interpolator import FadeInterpolator, LinearInterpolator
from engine.gamestate import norm_w, norm_h
from engine.util import make_dt_wrapper

# myscene is set by scene.py
myscene = None

# wait_time = lambda text: max(len(text)*0.015, 3.0)+3.0
wait_time = lambda text: 3.0

note_actor = None
can_continue = False

def init(fresh=True):
    myscene.ui.inventory.visible = False
    myscene.actors['pic'].sprite.opacity = 0
    myscene.play_music('sonata', fade=False)
    
    with pyglet.resource.file(myscene.resource_path('credits.yaml'), 'r') as f:
        t = 0
        for item in yaml.load(f):
            pyglet.clock.schedule_once(functools.partial(show_team_member, item['name'], item['role']), t)
            t += 6.0

def show_team_member(name, role, dt=0):
    a = myscene.actors['pic']
    a.update_state(name.split()[0].lower())
    
    px = random.random()*0.3+0.05
    a.x = random.randint(150, norm_w-150)
    if random.randint(0, 1) == 1:
        py = random.random()*0.2+0.6
        a.sprite.y = random.randint(150, norm_h/2-150)
    else:
        py = random.random()*0.2+0.1
        a.sprite.y = random.randint(norm_h/2+150, norm_h-150)
    
    spawn_text(name, 0.045, px, py)
    spawn_text(role, 0.035, px, py-0.06)
    
    interp = LinearInterpolator(a.sprite, 'opacity', start=0, end=255, 
                                name="fade", duration=2.0)
    
    myscene.add_interpolator(interp)
    
    def fade_out(dt=0):
        interp2 = LinearInterpolator(a.sprite, 'opacity', start=255, end=0, 
                                    name="fade2", duration=2.0)
        myscene.add_interpolator(interp2)
    
    pyglet.clock.schedule_once(fade_out, 4.0)

def spawn_text(text, size, x, y, dt=0):
    l = pyglet.text.Label(text, font_name=['Verdana', 'Helvetica'], font_size=norm_h*size, 
                          anchor_x='left', anchor_y='center', batch=myscene.batch,
                          color=(255, 255, 255, 255), x=norm_w*x, y=norm_h*y)
    if l.content_width > 960:
        l.delete()
        l = pyglet.text.Label(text, font_name=['Courier', 'Helvetica'], font_size=norm_h*size, 
                              anchor_x='left', anchor_y='center', batch=myscene.batch,
                              color=(255, 255, 255, 255), x=norm_w*x, y=norm_h*y,
                              multiline=True, width=960)
    def start_text():
        interp = FadeInterpolator(l, 'color', start=0, end=255, name="fade", duration=2.0)
        myscene.interp.add_interpolator(interp)
    
    def end_text(dt=0):
        interp = FadeInterpolator(l, 'color', start=255, end=0, name="fade", duration=2.0)
        myscene.interp.add_interpolator(interp)
    
    start_text()
    pyglet.clock.schedule_once(end_text, 4.0)
    return wait_time(text)+3

def transition_from(old_scene):
    pass

def handle_event(event, *args):
    pass

def actor_clicked(clicked_actor):
    pass
