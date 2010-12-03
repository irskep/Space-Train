import functools
import pyglet
import re
from time import sleep

from engine import actor
from engine.util import make_dt_wrapper
from engine.interpolator import LinearInterpolator

import state

@state.handles_walk('main')
def inga_walk(actor, point):
    if point == 'point_1':
        state.myscene.play_sound("door_open")
        state.myscene.handler.notify('act1_scene1')
    elif point == 'inga_exit':
        state.myscene.play_sound("door_open")
        state.myscene.handler.notify('act1_scene3')
    elif point == "point_2":
        if state.myscene.global_dict['groupies_blocked'] and \
        state.myscene.global_dict['potato_rolling']:
            state.myscene.begin_conversation("a_convenient_opening")
    elif point == "inga_attempt_stanislov":
        if not state.myscene.global_dict['guards_appeased']:
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
    if point == "meet_stanislav" and 'kidnap_stanislav' in state.myscene.global_dict and state.myscene.global_dict['kidnap_stanislav']:
        kidnap_stanislav()
        state.myscene.global_dict['kidnap_stanislav'] = False
            
            
def kidnap_stanislav():
    pyglet.resource.media('sound/lights_out.ogg', streaming=False).play()
    state.myscene.blackout = True
    state.myscene.fade_music(0)
    
    def scream(dt=0):
        pyglet.resource.media('sound/scream.wav', streaming=False).play()
    
    def flash_drag_away(dt=0):
        sb = state.myscene.actors['sneaky_bastard_1']
        pos = (state.myscene.actors['stanislav'].abs_position_x(), state.myscene.actors['stanislav'].abs_position_y())
        sb.walkpath_point = None
        sb.sprite.position = state.myscene.actors['stanislav'].sprite.position
        sb.update_state('kidnap_left')
        i = LinearInterpolator(sb.sprite, 'y', end=0, duration=1.5)
        state.myscene.remove_actor('stanislav')
        state.myscene.blackout = False
    
    def re_blackout(dt=0):
        state.myscene.blackout = True
        pyglet.resource.media('sound/clonk.mp3', streaming=False).play()
    
    def un_blackout(dt=0):
        mor = state.myscene.actors['moritz']
        mik = state.myscene.actors['mikhail']
        mor.update_state('knocked_out')
        mik.update_state('dizzy_stars')
        mik.casts_shadow = False
        mik.sprite.position = (mor.sprite.x, mor.sprite.y + 100)
        state.myscene.play_music("beethoven", fade=False)
        state.myscene.actors['tourist'].prepare_walkpath_move('tourist_inga')
        state.myscene.actors['tourist'].next_action()
        state.myscene.remove_actor('sneaky_bastard_1')
        state.myscene.blackout = False
    
    pyglet.clock.schedule_once(scream, 1.0)
    pyglet.clock.schedule_once(flash_drag_away, 2.5)
    pyglet.clock.schedule_once(re_blackout, 4.0)
    pyglet.clock.schedule_once(un_blackout, 7.0)

@state.handles_walk('tourist')
def tourist_to_inga(actor, point):
    if point == 'tourist_inga':
        state.myscene.begin_conversation("disaster_strikes")
    
@state.handles_walk('potato')
def potato_roll(actor, point):
    if point == "potato_15":
        state.myscene.interaction_enabled = True
    if point == "potato_9":
        state.myscene.actors['potato'].update_state("run_right")
        state.myscene.actors['potato'].prepare_walkpath_move("potato_15")
        state.myscene.actors['potato'].next_action()
        
@state.handles_walk('potato_drop')
def potato_drop(actor, point):
    if point == "potato_drop_end":
        squeak_snd = pyglet.resource.media('sound/squeak.wav', streaming=False)
        squeak_snd.play()
        
        actor.walk_speed = 200
        #stanislav is surprised at the critter
        pyglet.clock.schedule_once(make_dt_wrapper(state.myscene.begin_conversation), 1, "a_visitor")
    
        actor.update_state('run_note_4')
 
    if point == "shake_4":
        actor.prepare_walkpath_move('potato_exit')
        pyglet.clock.schedule_once(make_dt_wrapper(actor.next_action), 3)
        actor.update_state('run_4')
