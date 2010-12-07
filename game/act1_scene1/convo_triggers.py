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
    if state.myscene.global_dict.get('hamster_dropped', False):
        state.myscene.global_dict['hamster_dropped'] = True
        if not state.myscene.ui.inventory.has_item('potato') and not 'potato' in myscene.actors:
            potato = state.myscene.new_actor('potato', 'potato')
            potato.walkpath_point = "potato_32"
            potato.sprite.position = state.myscene.walkpath.points['potato_32']
            potato.prepare_walkpath_move("potato_10")
            potato.next_action()
            state.myscene.global_dict['potato_rolling'] = True
        
            shamus = state.myscene.actors['shamus']
            shamus.update_state('eating')
            shamus.walkpath_point = "shamus_sit"
            shamus.sprite.position = state.myscene.walkpath.points['shamus_sit']
        

@state.handles_convo('thermostat_discover')
def handle_thermostat():
    if state.myscene.handler.handler.game_variables['temperature'] >= 80:
        state.myscene.actors['thermostat'].update_state('rising')
        # Nicole complains!
        tourist = state.myscene.actors['tourist']
        pyglet.clock.schedule_once(make_dt_wrapper(tourist.prepare_walkpath_move), 5, "tourist_complain")
        pyglet.clock.schedule_once(tourist.next_action, 5)
