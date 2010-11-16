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
    myscene.handler.handler.game_variables['no_groupies_intro'] = False
    if fresh:
        myscene.actors['main'].prepare_walkpath_move("point_2")
        myscene.actors['main'].next_action()
        
def end_conversation(convo_name):
    if convo_name == "no_groupies_intro":
        myscene.begin_conversation("no_groupies")

def inga_walk(actor, point):
    mikhail = myscene.actors['mikhail']
    moritz = myscene.actors['moritz']
    if point == "point_2":
        myscene.begin_background_conversation("need_a_smoke")
    if point == "inga_attempt_stanislov":
        if myscene.background_convo_in_progress("need_a_smoke"):
            myscene.end_background_conversation("need_a_smoke")
        mikhail.prepare_walkpath_move("mikhail_guard")
        moritz.prepare_walkpath_move("moritz_guard")
        mikhail.next_action()
        moritz.next_action()
        if not myscene.handler.handler.game_variables['no_groupies_intro']:
            myscene.begin_conversation("no_groupies_intro")
        else:
            myscene.begin_conversation("no_groupies")
        
walk_handlers = {
    'main': inga_walk
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if actor.identifier == 'main' and point == 'point_1':
            myscene.handler.notify('act1_scene1')
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    pass
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point