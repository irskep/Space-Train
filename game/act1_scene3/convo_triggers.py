import functools
import pyglet

from engine.interpolator import Linear2DInterpolator
from engine.util import make_dt_wrapper

import state

@state.handles_convo('hipster_pass')
def handle_hipsters():
    state.myscene.actors['hipster_amanda'].prepare_walkpath_move('amanda_1')
    state.myscene.actors['hipster_amanda'].next_action()
    if not state.myscene.global_dict['deep_couch']:
        state.myscene.actors['main'].prepare_walkpath_move('point_1')
        state.myscene.actors['main'].next_action()
    else:
        state.myscene.begin_background_conversation('hipster_argument')
        state.myscene.interaction_enabled = True

@state.handles_convo('inspect_button')
def handle_button():
    if state.myscene.global_dict['button_pressed'] == True:
        state.myscene.actors['button'].update_state('ButtonOn')
        state.myscene.fade_music(time=0.0)
        state.myscene.play_sound('klaxon')
        state.myscene.begin_conversation('oops')

@state.handles_convo('oops')
def handle_oops():
    state.myscene.fade_music(0.95)
    state.myscene.fade_background(0.95)
    state.myscene.handler.notify('credits')

@state.handles_convo('amanda', 'amanda_1', 'fran', 'fran_1', 'liam', 'liam_1')
def handle_argument():
    myscene.begin_background_conversation('hipster_argument')
