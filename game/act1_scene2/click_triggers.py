import functools
import pyglet

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
