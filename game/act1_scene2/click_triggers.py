import functools
import pyglet

import state

@state.handles_click('nonexistent')
def talk_to_nobody(clicked_actor):
    pass