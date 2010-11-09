import pyglet
import functools
import re

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamestate
from engine import convo
from engine import util

# myscene is set by scene.py
myscene = None

levity_exposition = False
levity_direction = "right"

do_sit = False
sneelock_distracted = False

temperature = 72

def init(fresh=False):
    if fresh:
        myscene.actors['main'].prepare_walkpath_move("point_2")
        myscene.actors['main'].next_action()

def end_conversation(convo_name):
    pass

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        pass
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    pass
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point