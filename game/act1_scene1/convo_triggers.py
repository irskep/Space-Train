import functools
import pyglet

from engine.util import make_dt_wrapper

import state

@state.handles_convo('introduction')
def handle_intro():
    state.myscene.interaction_enabled = True
    state.myscene.actors['levity'].prepare_walkpath_move("levity_right")
    state.myscene.actors['levity'].next_action()
    state.myscene.handler.handler.save()
    state.myscene.actors['main'].update_state('sit')

@state.handles_convo('you_shall_not_pass')
def handle_block_door():
    state.myscene.actors['sneelock'].prepare_walkpath_move("sneelock_guard")
    state.myscene.actors['sneelock'].next_action()

    state.myscene.actors['main'].prepare_walkpath_move("point_6")
    state.myscene.actors['main'].next_action()
    
    state.myscene.handler.handler.save()

@state.handles_convo('its_too_hot')
def handle_complaint():
    state.myscene.actors['sneelock'].prepare_walkpath_move("sneelock_inspect")
    state.myscene.actors['sneelock'].next_action()

@state.handles_convo('a_young_irish_boy')
def handle_shamus():
    if state.myscene.handler.handler.game_variables.get('hamster_dropped', False):
        potato = state.myscene.new_actor('potato', 'potato')
        potato.walk_speed = 200.0
        potato.walkpath_point = "potato_9"
        potato.prepare_walkpath_move("potato_10")
        potato.next_action()
        state.myscene.handler.handler.game_variables['potato_rolling'] = True

@state.handles_convo('thermostat_discover')
def handle_thermostat():
    if state.myscene.handler.handler.game_variables['temperature'] >= 80:
        state.myscene.actors['thermostat'].update_state('rising')
        # Nicole complains!
        tourist = state.myscene.actors['tourist']
        pyglet.clock.schedule_once(make_dt_wrapper(tourist.prepare_walkpath_move), 5, "tourist_complain")
        pyglet.clock.schedule_once(tourist.next_action, 5)
