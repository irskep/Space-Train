import pyglet
import functools

from engine import actor
from engine.interpolator import FadeInterpolator
from engine.gamestate import norm_w, norm_h


# myscene is set by scene.py
myscene = None

def init(fresh=True):
    sequence = (
        ("It's the year 3030", 0.05, 0.5, 0.5),
        ("And here at the Corporate Institutional Bank of Time", 0.04, 0.5, 0.5),
        ("We find ourselves reflecting", 0.05, 0.5, 0.5),
        ("Finding out, that in fact, we came back", 0.04, 0.5, 0.5),
        ("We were always coming back...", 0.04, 0.5, 0.5),
    )
    show_sequence(sequence)

def show_sequence(sequence):
    sequence_item(sequence, 0, end_sequence)

def end_sequence():
    myscene.handler.notify('act1_scene1')

def sequence_item(sequence, item, final_callback, l=None, _=None):
    if l:
        l.delete()
    if item >= len(sequence):
        print 'done?'
        final_callback()
        return
    text, size, x, y = sequence[item]
    l = pyglet.text.Label(text, font_name='Helvetica', font_size=norm_h*size, 
                          anchor_x='center', anchor_y='baseline', batch=myscene.batch,
                          color=(255, 255, 255, 255), x=norm_w*x, y=norm_h*y)
    interp = FadeInterpolator(l, 'color', start=0, end=255, name="fade", duration=3.0, 
                                done_function=functools.partial(end_sequence_item, sequence, 
                                                                 item, final_callback, l))
    myscene.interp.add_interpolator(interp)

def end_sequence_item(sequence, item, final_callback, l, _=None):
    interp = FadeInterpolator(l, 'color', start=255, end=0, name="fade", duration=3.0, 
                                done_function=functools.partial(sequence_item, sequence, item+1,
                                                                 final_callback, l))
    myscene.interp.add_interpolator(interp)

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
    if clicked_actor.identifier == "logo":
        myscene.handler.notify("act1_scene1")
        interp = LinearInterpolator(clicked_actor.sprite, 'rotation', 0.0, 360, speed=500.0)
        myscene.add_interpolator(interp)
