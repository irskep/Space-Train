import pyglet
import functools
import re

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import camera
from engine import gamestate
from engine import convo
from engine import util

# myscene is set by scene.py
myscene = None

def init(fresh=False):
    if fresh:
        myscene.actors['main'].prepare_walkpath_move("point_2")
        myscene.actors['main'].next_action()
        
def end_conversation(convo_name):
    pass

def inga_walk(actor, point):
    if point == "point_2":
        myscene.begin_background_conversation("need_a_smoke")
        
walk_handlers = {
    'main': inga_walk
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    pass
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point