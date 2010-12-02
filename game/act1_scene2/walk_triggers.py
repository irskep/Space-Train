import functools
import pyglet
import re

from engine import actor
from engine.util import make_dt_wrapper

import state

@state.handles_walk('main')
def inga_walk(actor, point):
    if point == 'point_1':
        myscene.play_sound("door_open")
        myscene.handler.notify('act1_scene1')
    elif point == "point_2":
        if state.myscene.global_dict['groupies_blocked'] and \
        state.myscene.global_dict['potato_rolling']:
            state.myscene.begin_conversation("a_convenient_opening")
            state.myscene.global_dict['groupies_blocked'] = False
    elif point == "inga_attempt_stanislov":
        mikhail = state.myscene.actors['mikhail']
        moritz = state.myscene.actors['moritz']
        if state.myscene.background_convo_in_progress("need_a_smoke"):
            state.myscene.end_background_conversation("need_a_smoke")
        mikhail.prepare_walkpath_move("mikhail_guard")
        moritz.prepare_walkpath_move("moritz_guard")
        mikhail.next_action()
        moritz.next_action()
        if not state.myscene.global_dict['no_groupies_intro']:
            state.myscene.begin_conversation("no_groupies_intro")
        else:
            state.myscene.begin_conversation("no_groupies")

@state.handles_walk('potato')
def potato_roll(actor, point):
    if point == "potato_15":
        state.myscene.interaction_enabled = True
    if point == "potato_9":
        state.myscene.actors['potato'].update_state("run_right")
        state.myscene.actors['potato'].prepare_walkpath_move("potato_15")
        state.myscene.actors['potato'].next_action()
