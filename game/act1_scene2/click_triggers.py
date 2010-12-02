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
    state.myscene.ui.inventory.get_item('potato_note')
    def potato_drop():
        potato = state.myscene.actors['potato_drop']
        potato.prepare_walkpath_move('potato_drop_end')
        potato.next_action()

    state.start_cutscene()
    interp = Linear2DInterpolator(state.myscene.camera, 'position', (0.0, 360.0), 
                                  start_tuple=(1920,360), speed=400.0, 
                                  done_function=make_dt_wrapper(potato_drop))
    state.myscene.add_interpolator(interp)

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