from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator

# myscene is set by scene.py
myscene = None

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
