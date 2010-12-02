import functools
import pyglet

import state

@state.handles_click('hipster_amanda')
def talk_to_amanda(clicked_actor):
    state.myscene.end_background_conversation('hipster_argument')
    if state.myscene.actors['main'].walkpath_point == 'point_2':
        state.myscene.begin_conversation('amanda')
    elif state.myscene.actors['main'].walkpath_point == 'point_3':
        state.myscene.begin_conversation('amanda_l')

@state.handles_click('hipster_liam')
def talk_to_liam(clicked_actor):
    state.myscene.end_background_conversation('hipster_argument')
    if state.myscene.actors['main'].walkpath_point == 'point_2':
        state.myscene.begin_conversation('liam')
    elif state.myscene.actors['main'].walkpath_point == 'point_3':
        state.myscene.begin_conversation('liam_l')

@state.handles_click('hipster_fran')
def talk_to_fran(clicked_actor):
    state.myscene.end_background_conversation('hipster_argument')
    if state.myscene.actors['main'].walkpath_point == 'point_2':
        state.myscene.begin_conversation('fran')
    elif state.myscene.actors['main'].walkpath_point == 'point_3':
        state.myscene.begin_conversation('fran_l')

@state.handles_click('door')
def click_door(clicked_actor):
    state.myscene.begin_conversation("locked_door")

@state.handles_click('button')
def click_button(clicked_actor):
    inspect_func = functools.partial(state.myscene.begin_conversation, "inspect_button")
    state.myscene.ui.show_cam(clicked_actor, 
                              {'Inspect': inspect_func})
