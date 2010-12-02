import functools
import pyglet

from engine.interpolator import PulseInterpolator, LinearInterpolator, Linear2DInterpolator

import state
from engine import util

@state.handles_click('airduct')
def airduct_click(clicked_actor):
    options = {}
    options['Inspect'] = inspect_duct
    if state.myscene.ui.inventory.has_item('potato_note'):
        options['Send Potato on a journey'] = potato_adventure
    options['Looks a bit too dangerous'] = lambda: 1+1
    state.myscene.ui.show_cam(clicked_actor, options)
    
def inspect_duct():
    state.start_cutscene()
    interp = Linear2DInterpolator(state.myscene.camera, 'position', (0.0, 360.0), 
                                  start_tuple=(1920,360), speed=400.0, 
                                  done_function=util.make_dt_wrapper(state.end_cutscene))
    myscene.add_interpolator(interp)
    pass
    
def potato_adventure():
    pass

@state.handles_click('pen')
def pen_options(clicked_actor):
    if state.myscene.global_dict['groupies_blocked']:
        state.myscene.ui.show_cam(clicked_actor, {'Write a lovely note to Stanislav': make_note, 'Clicka-clicka': lambda: 1+1})

def make_note():
    state.myscene.ui.inventory.get_item('pen')
    state.myscene.ui.inventory.get_item('notepad')
    
    note = actor.Actor('note', 'note', state.myscene)
    state.myscene.ui.inventory.put_item(note)
