from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator

# myscene is set by scene.py
myscene = None

def init():
    title = myscene.actors['title']
    interp = PulseInterpolator(title.sprite, 'scale', 0.9, 1.0, speed=4)
    myscene.add_interpolator(interp)

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
    if clicked_actor.identifier == "logo":
        myscene.handler.notify("midterm2")
        interp = LinearInterpolator(clicked_actor.sprite, 'rotation', 0.0, 360, speed=500.0)
        myscene.add_interpolator(interp)
