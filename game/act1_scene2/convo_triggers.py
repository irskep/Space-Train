import functools
import pyglet

from engine.interpolator import Linear2DInterpolator
from engine.util import make_dt_wrapper

import state

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
        return_to_inga()

@state.handles_convo('a_convenient_opening')
def handle_duct():
    state.myscene.interaction_enabled = False
    potato = state.myscene.actors['potato']
    potato.walk_speed = 200.0
    potato.walkpath_point = "potato_1"
    potato.prepare_walkpath_move("potato_9")
    potato.next_action()
    
@state.handles_convo('airduct_inspect')
def inspect_duct():
    state.start_cutscene()
    interp = Linear2DInterpolator(state.myscene.camera, 'position', (0.0, 360.0), 
                                  start_tuple=(1920,360), speed=400.0, 
                                  done_function=make_dt_wrapper(return_to_inga))
    state.myscene.add_interpolator(interp)
    
def return_to_inga():
    x = state.myscene.actors['main'].abs_position_x()
    y = state.myscene.actors['main'].abs_position_y()
    interp = Linear2DInterpolator(state.myscene.camera, 'position',
            (x, y), speed=400.0, done_function=make_dt_wrapper(state.end_cutscene))
    state.myscene.add_interpolator(interp)

@state.handles_convo('write_note')
def potato_adventure():
    state.myscene.ui.inventory.get_item('potato_note')

    def potato_drop():
        potato = state.myscene.actors['potato_drop']
        potato.walk_speed = 800
        potato.prepare_walkpath_move('potato_drop_end')
        potato.next_action()

    state.start_cutscene()
    interp = Linear2DInterpolator(state.myscene.camera, 'position', (0.0, 360.0), 
                                  start_tuple=(1920,360), speed=400.0, 
                                  done_function=make_dt_wrapper(potato_drop))
    state.myscene.add_interpolator(interp)

@state.handles_convo('a_visitor')
def ball_drop():
    #pause for a moment, then shake it off
    state.myscene.actors['potato_drop'].prepare_walkpath_move('shake_4')
    pyglet.clock.schedule_once(make_dt_wrapper(state.myscene.actors['potato_drop'].next_action), 3)
    state.myscene.actors['potato_drop'].update_state('run')
    state.myscene.begin_conversation('surprise_note')
    
@state.handles_convo('surprise_note')
def stanislav_loves_inga():
    
    x = state.myscene.actors['main'].abs_position_x()
    y = state.myscene.actors['main'].abs_position_y()
    interp = Linear2DInterpolator(state.myscene.camera, 'position',
            (x, y), speed=400.0, done_function=make_dt_wrapper(inga_to_stanny))
    state.myscene.add_interpolator(interp)
    
def inga_to_stanny():
    mikhail = state.myscene.actors['mikhail']
    moritz = state.myscene.actors['moritz']
    
    mikhail.prepare_walkpath_move('mikhail_idle')
    mikhail.next_action()
    
    moritz.prepare_walkpath_move('moritz_idle')
    moritz.next_action()

    state.myscene.global_dict['guards_appeased'] = True
    state.myscene.global_dict['groupies_blocked'] = False
    
    state.myscene.moving_camera = False
    inga = state.myscene.actors['main']
    inga.prepare_walkpath_move('meet_stanislav')
    inga.next_action()
    
    state.myscene.global_dict['kidnap_stanislav'] = True
    
@state.handles_convo('disaster_strikes')
def disaster_struck():
    state.myscene.actors['tourist'].prepare_walkpath_move('tourist_start')
    state.myscene.actors['tourist'].next_action()
    state.end_cutscene()