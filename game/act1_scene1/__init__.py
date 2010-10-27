import functools

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

# myscene is set by scene.py
myscene = None

def init():
    myscene.ui.inventory.visible = True
    myscene.actors['levity'].prepare_walkpath_move("levity_inga")
    myscene.actors['levity'].next_action()
    #text.init(myscene)

def inga_walk(actor, point):
    pass
    
def levity_walk(actor, point):
    if point == "levity_inga":
        #begin convo
        print "updating state"
        actor.update_state("stand_right")
    
def ask_about_beans():
    myscene.convo.begin_conversation('beans_1')
    bean_salesman = myscene.actors['bean_salesman']

def end_conversation(convo_name):
    myscene.actors['main'].update_state('stand_front')

walk_handlers = {
    'main': inga_walk,
    'levity': levity_walk
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):    
    print "Clicked on %s" % clicked_actor.name