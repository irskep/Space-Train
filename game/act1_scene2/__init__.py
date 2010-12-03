import pyglet
import functools
import re

import state
import convo_triggers
import click_triggers
import walk_triggers

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator, Linear2DInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import util

# myscene is set by scene.py
myscene = None

def init(fresh=False):
    state.myscene = myscene
    myscene.global_dict['no_groupies_intro'] = False
    myscene.global_dict['guards_appeased'] = False
    myscene.global_dict['groupies_blocked'] = False
        
    myscene.play_music('bach', fade=False)
    if fresh:
        # potato_note = actor.Actor('potato_note', 'potato', state.myscene)
        # potato_note.anchor_x = 0.0
        # potato_note.update_state('sit')
        # state.myscene.ui.inventory.put_item(potato_note)
        
        walk_from_right()
        
        #pan to show the guards        
        queue_need_a_smoke()


def queue_need_a_smoke():
    def begin_smoke_conv():
        myscene.begin_conversation("need_a_smoke")
    
    state.start_cutscene()
    interp = Linear2DInterpolator(myscene.camera, 'position', (0.0, 360.0), 
                                  start_tuple=(1920,360), speed=400.0, 
                                  done_function=util.make_dt_wrapper(begin_smoke_conv))
    myscene.add_interpolator(interp)

@state.handles_transition('act1_scene1')
def come_from_right():
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
    if point == 'meet_stanislav' or point == 'inga_exit':
        if not state.myscene.global_dict['guards_appeased']:
            return 'inga_attempt_stanislov'
        else:
            return point
    else:
        return point
