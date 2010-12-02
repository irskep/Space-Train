import functools
import pyglet

from engine.interpolator import Linear2DInterpolator
from engine.util import make_dt_wrapper

import state

def end_cutscene():
    state.myscene.interaction_enabled = True
    state.myscene.moving_camera = False

@state.handles_convo('no_groupies_intro')
def handle_groupies_intro():
    state.myscene.begin_conversation("no_groupies")

@state.handles_convo('no_groupies')
def handle_groupies():
    if state.myscene.global_dict['guards_appeased']:
        state.myscene.global_dict['groupies_blocked'] = False
        state.myscene.actors['mikhail'].prepare_walkpath_move("mikhail_idle")
        state.myscene.actors['mikhail'].next_action()
        state.myscene.actors['moritz'].prepare_walkpath_move("moritz_idle")
        state.myscene.actors['moritz'].next_action()
    else:
        state.myscene.global_dict['groupies_blocked'] = True

@state.handles_convo('need_a_smoke')
def handle_small_talk():
    if not state.myscene.interaction_enabled and state.myscene.moving_camera:
        x = state.myscene.actors['main'].abs_position_x()
        y = state.myscene.actors['main'].abs_position_y()
        interp = Linear2DInterpolator(state.myscene.camera, 'position',
                (x, y), speed=400.0, done_function=make_dt_wrapper(end_cutscene))
        pyglet.clock.schedule_once(make_dt_wrapper(state.myscene.add_interpolator), 1, interp)

@state.handles_convo('a_convenient_opening')
def handle_duct():
    state.myscene.interaction_enabled = False
    potato = state.myscene.actors['potato']
    potato.walk_speed = 200.0
    potato.walkpath_point = "potato_1"
    potato.prepare_walkpath_move("potato_9")
    potato.next_action()
