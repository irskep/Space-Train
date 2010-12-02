import functools
import pyglet

from engine import actor

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

@state.handles_click('potato')
def potato_options(clicked_actor):
    if state.myscene.ui.inventory.has_item("note"):
        state.myscene.handler.handler.game_variables['potato_stop'] = True
        state.myscene.ui.show_cam(clicked_actor, {'Hijack potato for your own nefarious purposes': note_potato, 'Keep rollin\' little buddy!': resume_potato_roll})

def resume_potato_roll():
    state.myscene.global_dict['potato_stop'] = False
        
def note_potato():
    state.myscene.actors['potato'].update_state("run_note")
    state.myscene.remove_actor('potato')
    
    state.myscene.ui.inventory.get_item('note')
    
    potato_note = actor.Actor('potato_note', 'potato', state.myscene)
    potato_note.anchor_x = 0.0
    potato_note.update_state('sit_note')
    state.myscene.ui.inventory.put_item(potato_note)
    
@state.handles_click('thermostat')
def thermostat_options(clicked_actor):
    inspect_func = functools.partial(state.myscene.begin_conversation, "thermostat_discover")
    state.myscene.ui.show_cam(state.myscene.actors['thermostat'], {'Inspect': inspect_func})

@state.handles_click('pen')
def pen_options(clicked_actor):
    if state.myscene.global_dict['groupies_blocked']:
        state.myscene.ui.show_cam(clicked_actor, {'Write a lovely note to Stanislav': make_note, 'Clicka-clicka': lambda: 1+1})

def make_note():
    state.myscene.ui.inventory.get_item('pen')
    state.myscene.ui.inventory.get_item('notepad')
    
    state.myscene.begin_conversation("write_note")
    
    note = actor.Actor('note', 'note', state.myscene)
    state.myscene.ui.inventory.put_item(note)