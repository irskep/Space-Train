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
    myscene.ui.inventory.visible = True
    myscene.handler.handler.game_variables['deep_couch'] = False
    
    myscene.play_music('deepcouch', fade=False)
    myscene.play_background('Train_Loop1', fade=True)
    
    walk_from_right()

def walk_from_right():
    myscene.actors['main'].walkpath_point = 'point_1'
    myscene.actors['main'].prepare_walkpath_move('point_2')
    myscene.actors['main'].next_action()
        
def end_conversation(convo_name):
    if convo_name == "hipster_pass":
        if not myscene.handler.handler.game_variables['deep_couch']:
            myscene.actors['main'].prepare_walkpath_move('point_1')
            myscene.actors['main'].next_action()
        else:
            myscene.interaction_enabled = True
            
def inga_walk(actor, point):
    if point == "point_2" and not myscene.handler.handler.game_variables['deep_couch']:
        myscene.begin_conversation("hipster_pass")
        
walk_handlers = {
    'main': inga_walk
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if actor.identifier == 'main' and point == 'point_1':
            myscene.handler.notify('act1_scene2')
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    pass
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point