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
    
    myscene.play_music('deepcouch', fade=False)
    myscene.play_background('Train_Loop1', fade=True)
    
    if fresh:
        myscene.handler.handler.game_variables['deep_couch'] = False
        myscene.handler.handler.game_variables['button_inspected'] = False
        myscene.handler.handler.game_variables['button_pressed'] = False
    else:
        myscene.interaction_enabled = True

def walk_from_right():
    myscene.actors['main'].walkpath_point = 'point_1'
    myscene.actors['main'].prepare_walkpath_move('point_2')
    myscene.actors['main'].next_action()
        
def end_conversation(convo_name):
    if convo_name == "hipster_pass":
        myscene.actors['hipster_amanda'].prepare_walkpath_move('amanda_1')
        myscene.actors['hipster_amanda'].next_action()
        if not myscene.handler.handler.game_variables['deep_couch']:
            myscene.actors['main'].prepare_walkpath_move('point_1')
            myscene.actors['main'].next_action()
        else:
            myscene.interaction_enabled = True
    elif convo_name == 'inspect_button' and myscene.handler.handler.game_variables['button_pressed'] == True:
        myscene.fade_music(time=0.0)
        myscene.play_sound('klaxon')
        myscene.begin_conversation('oops')
    elif convo_name == 'oops':
        myscene.play_sound('space_train_explode')
        #myscene.handler.notify('credits')
            
def inga_walk(actor, point):
    if point == "point_2" and not myscene.handler.handler.game_variables['deep_couch']:
        myscene.actors['hipster_amanda'].prepare_walkpath_move('amanda_2')
        myscene.actors['hipster_amanda'].next_action()
        myscene.begin_conversation("hipster_pass")
        
walk_handlers = {
    'main': inga_walk
}

def transition_from(old_scene):
    walk_from_right()

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
    
def talk_to_amanda():
    #myscene.end_background_conversation('hipster_argument')
    print myscene.actors['main'].walkpath_point
    if myscene.actors['main'].walkpath_point == 'point_2':
        myscene.begin_conversation('amanda')
    elif myscene.actors['main'].walkpath_point == 'point_3':
        myscene.begin_conversation('amanda_l')

def actor_clicked(clicked_actor):
    print clicked_actor
    
    click_handlers = {
        "hipster_amanda": talk_to_amanda,
        "button": functools.partial(myscene.ui.show_cam, clicked_actor, {'Inspect': functools.partial(myscene.begin_conversation, "inspect_button")})
    }
    
    if click_handlers.has_key(clicked_actor.identifier):
        click_handlers[clicked_actor.identifier]()
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point