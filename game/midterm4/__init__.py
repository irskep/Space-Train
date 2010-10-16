import functools

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

import text

# myscene is set by scene.py
myscene = None

def init():
    myscene.ui.inventory.visible = False
    text.init(myscene)

def end_conversation(convo_name):
    pass

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    text.advance()
    # myscene.ui.show_cam(clicked_actor, actions)
