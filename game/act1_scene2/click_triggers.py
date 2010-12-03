import functools
import pyglet

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator, Linear2DInterpolator
from engine.util import make_dt_wrapper

import state

@state.handles_click('airduct')
def airduct_click(clicked_actor):
    options = {}
    options['Inspect'] = inspect_duct
    if state.myscene.ui.inventory.has_item('potato_note'):
        options['Send Potato on a journey'] = potato_adventure
    options['Looks a bit too dangerous'] = lambda: 1+1
    state.myscene.ui.show_cam(clicked_actor, options)
    
def inspect_duct():
    state.myscene.begin_conversation("airduct_inspect")

def potato_adventure():
    state.myscene.begin_conversation('write_note')
    state.myscene.convo.next_line()

@state.handles_click('potato')
def potato_options(clicked_actor):
    state.myscene.handler.handler.game_variables['potato_stop'] = True
    state.myscene.ui.show_cam(clicked_actor, {'Hijack potato for your own nefarious purposes': note_potato, 'Keep rollin\' little buddy!': resume_potato_roll})

def resume_potato_roll():
    state.myscene.global_dict['potato_stop'] = False
        
def note_potato():
    state.myscene.actors['potato'].update_state("run_note")
    state.myscene.remove_actor('potato')
    
    potato_note = actor.Actor('potato_note', 'potato', state.myscene)
    potato_note.anchor_x = 0.0
    potato_note.update_state('sit')
    state.myscene.ui.inventory.put_item(potato_note)