import pyglet
import functools
import re

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator, Linear2DInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamestate
from engine import convo
from engine import util

# myscene is set by scene.py
myscene = None

def init(fresh=False):
    myscene.handler.handler.game_variables['no_groupies_intro'] = False
    myscene.handler.handler.game_variables['guards_appeased'] = False
    myscene.handler.handler.game_variables['groupies_blocked'] = False
        
    myscene.play_music('bach', fade=False)
    if fresh:
        walk_from_right()
        
        #pan to show the guards        
        queue_need_a_smoke()
        
def transition_from(old_scene):
    if old_scene == 'act1_scene1':
        walk_from_right()

def walk_from_right():
    myscene.actors['main'].walkpath_point = 'point_1'
    myscene.actors['main'].prepare_walkpath_move('point_2')
    myscene.actors['main'].next_action()
     
def begin_smoke_conv():
    myscene.begin_conversation("need_a_smoke")
     
def queue_need_a_smoke():
    pyglet.clock.schedule_once(util.make_dt_wrapper(start_cutscene), 0)
    interp = Linear2DInterpolator(myscene.camera, 'position', (0,0), speed=400.0, done_function=util.make_dt_wrapper(begin_smoke_conv))
    pyglet.clock.schedule_once(util.make_dt_wrapper(myscene.add_interpolator), 3, interp)
    
def start_cutscene():
    myscene.interaction_enabled = False
    myscene.moving_camera = True
    
def end_cutscene():
    myscene.interaction_enabled = True
    myscene.moving_camera = False
    
def end_conversation(convo_name):
    if convo_name == "no_groupies_intro":
        myscene.begin_conversation("no_groupies")
    if convo_name == "no_groupies":
        if myscene.handler.handler.game_variables['guards_appeased']:
            myscene.handler.handler.game_variables['groupies_blocked'] = False
            myscene.actors['mikhail'].prepare_walkpath_move("mikhail_idle")
            myscene.actors['mikhail'].next_action()
            myscene.actors['moritz'].prepare_walkpath_move("moritz_idle")
            myscene.actors['moritz'].next_action()
        else:
            myscene.handler.handler.game_variables['groupies_blocked'] = True
    if convo_name == "need_a_smoke":
        if not myscene.interaction_enabled and myscene.moving_camera:
            interp = Linear2DInterpolator(myscene.camera, 'position', (myscene.actors['main'].abs_position_x(), myscene.actors['main'].abs_position_y()), speed=400.0, done_function=util.make_dt_wrapper(end_cutscene))
            pyglet.clock.schedule_once(util.make_dt_wrapper(myscene.add_interpolator), 1, interp)
    if convo_name == "a_convenient_opening":
        myscene.interaction_enabled = False
        potato = myscene.actors['potato']
        potato.walk_speed = 200.0
        potato.walkpath_point = "potato_1"
        potato.prepare_walkpath_move("potato_9")
        potato.next_action()
            
def inga_walk(actor, point):
    mikhail = myscene.actors['mikhail']
    moritz = myscene.actors['moritz']
    if point == "point_2":
        if myscene.handler.handler.game_variables['groupies_blocked'] and myscene.handler.handler.game_variables['potato_rolling']:
            myscene.begin_conversation("a_convenient_opening")
            myscene.handler.handler.game_variables['groupies_blocked'] = False
    if point == "inga_attempt_stanislov":
        if myscene.background_convo_in_progress("need_a_smoke"):
            myscene.end_background_conversation("need_a_smoke")
        mikhail.prepare_walkpath_move("mikhail_guard")
        moritz.prepare_walkpath_move("moritz_guard")
        mikhail.next_action()
        moritz.next_action()
        if not myscene.handler.handler.game_variables['no_groupies_intro']:
            myscene.begin_conversation("no_groupies_intro")
        else:
            myscene.begin_conversation("no_groupies")
        
def potato_roll(actor, point):
    if point == "potato_15":
        myscene.interaction_enabled = True
    if point == "potato_9":
        myscene.actors['potato'].update_state("run_right")
        myscene.actors['potato'].prepare_walkpath_move("potato_15")
        myscene.actors['potato'].next_action()
        
walk_handlers = {
    'main': inga_walk,
    'potato': potato_roll
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if actor.identifier == 'main' and point == 'point_1':
            myscene.handler.notify('act1_scene1')
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    pass
    
def give_actor(actor, item):
    return False
    
def filter_move(point):
    return point