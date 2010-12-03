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
