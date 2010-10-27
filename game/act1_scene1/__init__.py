import functools

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

# myscene is set by scene.py
myscene = None

levity_exposition = False

def init():
    myscene.ui.inventory.visible = True
    myscene.actors['levity'].prepare_walkpath_move("levity_4")
    myscene.actors['levity'].next_action()

def inga_walk(actor, point):
    pass
    
def levity_walk(actor, point):
    levity =  myscene.actors['levity']
    if point == "levity_left":
        levity.prepare_walkpath_move("levity_1")
        myscene.clock.schedule_once(levity.next_action, 60)
    if point == "levity_right":
        levity.prepare_walkpath_move("levity_4")
        myscene.clock.schedule_once(levity.next_action, 60)
    if point == "levity_1":
        
    if point == "levity_4":
        #begin convo
        actor.update_state("stand_right")
        myscene.convo.begin_conversation("introduction")
    
def ask_about_beans():
    myscene.convo.begin_conversation('beans_1')
    bean_salesman = myscene.actors['bean_salesman']

def end_conversation(convo_name):
    if convo_name == "introduction":   
        # Create the items to be given to Inga
        nuts = actor.Actor("tasty_nuts", "tasty_nuts", scene = myscene, attrs = {'start_state': 'tasty_nuts'})
        myscene.add_actor(nuts)
        myscene.ui.inventory.put_item(nuts)
        
        lemonade = actor.Actor("lemonade", "lemonade", scene = myscene, attrs = {'start_state': 'lemonade'})
        myscene.add_actor(lemonade)
        myscene.ui.inventory.put_item(lemonade)
        
        myscene.convo.begin_conversation("introduction_continued")

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