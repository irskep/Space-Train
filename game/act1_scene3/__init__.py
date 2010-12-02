import pyglet
import functools
import re

import state
import convo_triggers
import click_triggers
import walk_triggers

from engine.util.const import WALK_PATH_COMPLETED

# myscene is set by scene.py
myscene = None

def init(fresh=False):
    state.myscene = myscene
    myscene.ui.inventory.visible = True
    
    myscene.play_music('deepcouch', fade=False)
    
    if fresh:
        myscene.handler.handler.game_variables['deep_couch'] = False
        myscene.handler.handler.game_variables['button_inspected'] = False
        myscene.handler.handler.game_variables['button_pressed'] = False
        walk_from_right()
    else:
        myscene.begin_background_conversation('hipster_argument')
        myscene.interaction_enabled = True

@state.handles_transition('act1_scene2')
def come_from_right(old_scene):
    walk_from_right()

def walk_from_right():
    myscene.actors['main'].walkpath_point = 'point_1'
    myscene.actors['main'].prepare_walkpath_move('point_2')
    myscene.actors['main'].next_action()

def transition_from(old_scene):
    if state.transition_handlers.has_key(old_scene):
        state.transition_handlers[old_scene]()

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
        state.click_handlers[clicked_actor.identifier](clicked_actor)
    
def filter_move(point):
    return point
