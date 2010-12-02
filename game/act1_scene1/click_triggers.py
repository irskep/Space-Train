import functools
import pyglet

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamehandler
from engine import gamestate
from engine import convo
from engine import util

import state

@state.handles_click('shamus')
def talk_to_shamus(clicked_actor):
    state.myscene.begin_conversation('a_young_irish_boy')

@state.handles_click('gregg_briggs')
def talk_to_briggs(clicked_actor):
    state.myscene.end_background_conversation('mumblestiltskin')
    state.myscene.begin_conversation("briggs_exposition")

@state.handles_click('tourist', 'tourist_1')
def talk_to_tourists(clicked_actor):
    if state.myscene.actors['tourist'].walkpath_point == "tourist_start":
        state.myscene.begin_conversation("meet_the_tourists")

@state.handles_click('hipster_amanda', 'hipster_liam', 'hipster_fran')
def talk_to_hipsters(clicked_actor):
    if not state.sneelock_distracted:
        state.myscene.begin_conversation("grunt")

@state.handles_click('potato')
def potato_options(clicked_actor):
    if state.myscene.ui.inventory.has_item("note"):
        state.myscene.handler.handler.game_variables['potato_stop'] = True

@state.handles_click('thermostat')
def thermostat_options(clicked_actor):
    inspect_func = functools.partial(state.myscene.begin_conversation, "thermostat_discover")
    state.myscene.ui.show_cam(state.myscene.actors['thermostat'], {'Inspect': inspect_func})

@state.handles_click('pen')
def pen_options(clicked_actor):
    if state.myscene.global_dict['groupies_blocked']:
        state.myscene.ui.inventory.show_cam(clicked_actor, {'Write a lovely note to Stanislav': make_note, 'Clicka-clicka': lambda: 1+1})

def make_note(clicked_actor):
    state.myscene.ui.inventory.get_item('pen')
    state.myscene.ui.inventory.get_item('notepad')
    
    note = actor.Actor('note', 'note', state.myscene)
    state.myscene.ui.inventory.put_item(note)