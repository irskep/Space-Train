import pyglet
import functools
import re

import convo_triggers
import click_triggers
from convo_triggers import *
from click_triggers import *

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamehandler
from engine import gamestate
from engine import convo
from engine import util

# myscene is set by scene.py
myscene = None

levity_exposition = False
levity_direction = "right"

do_sit = False
sneelock_distracted = False

def init(fresh=False):
    convo_triggers.myscene = myscene
    click_triggers.myscene = myscene
    myscene.ui.inventory.visible = True
    
    myscene.begin_background_conversation("mumblestiltskin")
    
    myscene.play_music('simple', fade=False)
    myscene.play_background('Train_Loop1', fade=True)
    
    if fresh:
        myscene.handler.handler.game_variables['temperature'] = 72
        myscene.handler.handler.game_variables['potato_rolling'] = False
        myscene.handler.handler.game_variables['potato_stop'] = False
        myscene.interaction_enabled = False
        myscene.actors['levity'].prepare_walkpath_move("levity_4")
        myscene.actors['levity'].next_action()
    
        # spcbux = myscene.new_actor('space_bucks', 'space_bucks')
        spcbux = actor.Actor('space_bucks', 'space_bucks', myscene)
        myscene.ui.inventory.put_item(spcbux)
        
        pen = actor.Actor('pen', 'pen', myscene)
        myscene.ui.inventory.put_item(pen)
        
        notepad = actor.Actor('notepad', 'notepad', myscene)
        myscene.ui.inventory.put_item(notepad)
        
    else:
        myscene.interaction_enabled = True

def transition_from(old_scene):
    if old_scene == 'act1_scene2':
        myscene.interaction_enabled = True
        myscene.actors['main'].walkpath_point = 'transition_left'
        myscene.actors['main'].sprite.position = myscene.walkpath.points['transition_left']
        myscene.actors['main'].prepare_walkpath_move('inga_attempt_silver_class')
        myscene.actors['main'].next_action()
        
        if myscene.handler.handler.game_variables['potato_rolling']:
            myscene.actors['potato'].prepare_walkpath_move("potato_40")
            myscene.actors['potato'].next_action()
        
        myscene.actors['levity'].prepare_walkpath_move("levity_right")
        myscene.actors['levity'].next_action()

def inga_sit(seat):
    global do_sit
    inga = myscene.actors['main']
    inga.prepare_walkpath_move(seat.identifier)
    inga.next_action()
    do_sit = True

def end_conversation(convo_name):
    if convo_name == "introduction":
        myscene.interaction_enabled = True
        myscene.actors['levity'].prepare_walkpath_move("levity_right")
        myscene.actors['levity'].next_action()
        myscene.handler.handler.save()
        myscene.actors['main'].update_state('sit')

    if convo_name == "you_shall_not_pass":
        myscene.actors['sneelock'].prepare_walkpath_move("sneelock_guard")
        myscene.actors['sneelock'].next_action()

        myscene.actors['main'].prepare_walkpath_move("point_6")
        myscene.actors['main'].next_action()
        
        myscene.handler.handler.save()
    
    if convo_name == "its_too_hot":
        myscene.actors['sneelock'].prepare_walkpath_move("sneelock_inspect")
        myscene.actors['sneelock'].next_action()
        myscene.handler.handler.save()
        
    if convo_name == "a_young_irish_boy" and \
    myscene.handler.handler.game_variables.get('hamster_dropped', False):
        potato = myscene.new_actor('potato', 'potato')
        potato.walk_speed = 200.0
        potato.walkpath_point = "potato_9"
        potato.prepare_walkpath_move("potato_10")
        potato.next_action()
        myscene.handler.handler.game_variables['potato_rolling'] = True
    
    if convo_name == "thermostat_discover":
        if myscene.handler.handler.game_variables['temperature'] >= 80:
            myscene.actors['thermostat'].update_state('rising')
            # Nicole complains!
            tourist = myscene.actors['tourist']
            pyglet.clock.schedule_once(util.make_dt_wrapper(tourist.prepare_walkpath_move), 5, "tourist_complain")
            pyglet.clock.schedule_once(tourist.next_action, 5)

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        
        walk_handlers = {
            'main': inga_walk,
            'levity': levity_walk,
            'tourist': tourist_walk,
            'sneelock': sneelock_walk,
            'potato': potato_roll,
        }
        
        info = args[0]
        actor = info['actor']
        point = info['point']
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    if click_handlers.has_key(clicked_actor.identifier):
        click_handlers[clicked_actor.identifier]()

def filter_move(point):
    if point == "transition_left" and not sneelock_distracted:
        return "inga_attempt_silver_class"
    else:
        return point
