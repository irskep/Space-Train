import functools
import pyglet
import re

from engine import actor
from engine.util import make_dt_wrapper

import state

@state.handles_walk('main')
def inga_walk(actor, point):
    if point == "inga_attempt_silver_class":
        if not state.myscene.global_dict.get('sneelock_distracted', False):
            sneelock = state.myscene.actors['sneelock']
            sneelock.prepare_walkpath_move("sneelock_block")
            sneelock.next_action()
            state.myscene.convo.begin_conversation("you_shall_not_pass")
    if point == "transition_left":
        state.myscene.play_sound("door_open")
        state.myscene.handler.notify("act1_scene2")

@state.handles_walk('levity')
def levity_walk(actor, point):
    print "Walk handler called..."
    
    levity = state.myscene.actors['levity']
    next_point = point
    if point == "levity_left" or point == "levity_right":   
        if point == "levity_left":
            state.myscene.global_dict['levity_direction'] = 'right'
            next_point = "levity_1"
        elif point == "levity_right":
            state.myscene.global_dict['levity_direction'] = 'left'
            next_point = "levity_4"
        #levity.prepare_walkpath_move(next_point)
        pyglet.clock.schedule_once(make_dt_wrapper(levity.prepare_walkpath_move), 1, next_point)
        pyglet.clock.schedule_once(levity.next_action, 60)
        
    else:
        if point == "levity_1":
            next_point = "levity_2" if state.myscene.global_dict['levity_direction'] == "right" else "levity_left"
        elif point == "levity_2":
            next_point = "levity_3" if state.myscene.global_dict['levity_direction'] == "right" else "levity_1"
        elif point == "levity_3":
            next_point = "levity_4" if state.myscene.global_dict['levity_direction'] == "right" else "levity_2"
        elif point == "levity_4":
            if state.myscene.global_dict.get('levity_exposition', False) == False:
                state.myscene.global_dict['levity_exposition'] = True
                #begin convo
                actor.update_state("stand_right")
                state.myscene.begin_conversation("introduction")
            else:
                next_point = "levity_right" if state.myscene.global_dict['levity_direction'] == "right" else "levity_3"
        
        if next_point is not point:    
            levity.prepare_walkpath_move(next_point)
            print "Moving from %s to %s..." % (point, next_point)

@state.handles_walk('tourist')
def tourist_walk(actor, point):
    if point == "tourist_complain":
        state.myscene.global_dict['sneelock_distracted'] = True
        state.myscene.handler.handler.save()
        state.myscene.begin_background_conversation("its_too_hot")

@state.handles_walk('sneelock')
def sneelock_walk(actor, point):
    if point == "sneelock_inspect":
        pyglet.clock.schedule_once(make_dt_wrapper(state.myscene.begin_background_conversation), 5, "sneelock_checks_it_out")

@state.handles_walk('potato')  
def potato_roll(actor, point):
    point_match = re.search(r"potato_(\d+)", point)
    if point_match and not state.myscene.handler.handler.game_variables['potato_stop']:
        current_index = int(point_match.group(1))
        next_index = current_index + 1
        if next_index > 40:
            next_index = 1
        next_point = "potato_%d" % next_index
        print "Potato rolling from %s to %s" % (point, next_point)
        pyglet.clock.schedule_once(make_dt_wrapper(actor.prepare_walkpath_move), 0, next_point)
        pyglet.clock.schedule_once(make_dt_wrapper(actor.next_action), 0)
