import functools
import pyglet
import re

from engine import actor
from engine.util import make_dt_wrapper

import state

@state.handles_walk('main')
def inga_walk(actor, point):
    if point == 'point_1':
        state.myscene.handler.notify('act1_scene2')
    elif point == "point_2" and not state.myscene.global_dict['deep_couch']:
        state.myscene.actors['hipster_amanda'].prepare_walkpath_move('amanda_2')
        state.myscene.actors['hipster_amanda'].next_action()
        state.myscene.begin_conversation("hipster_pass")
