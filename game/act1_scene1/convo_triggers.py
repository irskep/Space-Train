from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamehandler
from engine import gamestate
from engine import convo
from engine import util

click_handlers = {}

def handles_click(f, *labels):
    for label in labels:
        click_handlers[label] = f
    return f

@handles_click('shamus')
def talk_to_shamus():
    myscene.begin_conversation('a_young_irish_boy')

@handles_click('gregg_briggs')
def talk_to_briggs():
    myscene.end_background_conversation('mumblestiltskin')
    myscene.begin_conversation("briggs_exposition")

@handles_click('tourist', 'tourist_1')
def talk_to_tourists():
    if myscene.actors['tourist'].walkpath_point == "tourist_start":
        myscene.begin_conversation("meet_the_tourists")

@handles_click('hipster_amanda', 'hipster_liam', 'hipster_fran')
def talk_to_hipsters():
    if not sneelock_distracted:
        myscene.begin_conversation("grunt")

@handles_click('potato')
def potato_options():
    if myscene.ui.inventory.has_item("note"):
        myscene.handler.handler.game_variables['potato_stop'] = True

@handles_click('thermostat')
def thermostat_options():
    inspect_func = functools.partial(myscene.begin_conversation, "thermostat_discover")
    myscene.ui.show_cam(clicked_actor, {'Inspect': inspect_func})
