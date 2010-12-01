import pyglet
import functools

import state
import convo_triggers
import click_triggers
import walk_triggers

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamehandler
from engine import gamestate
from engine import convo
from engine import util

# myscene is set by scene.py
myscene = None

def init(fresh=False):
    state.myscene = myscene
    myscene.ui.inventory.visible = True
    
    myscene.begin_background_conversation("mumblestiltskin")
    
    myscene.play_music('simple', fade=False)
    myscene.play_background('Train_Loop1', fade=True)
    
    if fresh:
        myscene.handler.handler.game_variables['temperature'] = 72
        myscene.handler.handler.game_variables['potato_rolling'] = False
        myscene.handler.handler.game_variables['potato_stop'] = False
        myscene.interaction_enabled = False
        myscene.actors['levity'].prepare_walkpath_move("levity_4")
        myscene.actors['levity'].next_action()
    
        # spcbux = myscene.new_actor('space_bucks', 'space_bucks')
        spcbux = actor.Actor('space_bucks', 'space_bucks', myscene)
        myscene.ui.inventory.put_item(spcbux)
        
        pen = actor.Actor('pen', 'pen', myscene)
        myscene.ui.inventory.put_item(pen)
        
        notepad = actor.Actor('notepad', 'notepad', myscene)
        myscene.ui.inventory.put_item(notepad)
        
    else:
        myscene.interaction_enabled = True

@state.handles_transition('act1_scene2')
def come_from_left():
    myscene.interaction_enabled = True
    myscene.actors['main'].walkpath_point = 'transition_left'
    myscene.actors['main'].sprite.position = myscene.walkpath.points['transition_left']
    myscene.actors['main'].prepare_walkpath_move('inga_attempt_silver_class')
    myscene.actors['main'].next_action()
    
    if myscene.handler.handler.game_variables['potato_rolling']:
        myscene.actors['potato'].prepare_walkpath_move("potato_40")
        myscene.actors['potato'].next_action()
    
    myscene.actors['levity'].prepare_walkpath_move("levity_right")
    myscene.actors['levity'].next_action()

def transition_from(old_scene):
    if state.transition_handlers.has_key(old_scene):
        state.transition_handlers[old_Scene]()

def end_conversation(convo_name):
    if state.convo_handlers.has_key(convo_name):
        state.convo_handlers[convo_name]()

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if state.walk_handlers.has_key(actor.identifier):
            state.walk_handlers[actor.identifier](actor, point)

def actor_clicked(clicked_actor):
    if state.click_handlers.has_key(clicked_actor.identifier):
        state.click_handlers[clicked_actor.identifier]()

def filter_move(point):
    if point == "transition_left" and not state.sneelock_distracted:
        return "inga_attempt_silver_class"
    else:
        return point
