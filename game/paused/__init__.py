from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator

# myscene is set by scene.py
myscene = None

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
    if clicked_actor.identifier == "exit":
        myscene.handler.notify("exit_game")
    if clicked_actor.identifier == "continue":
        myscene.handler.notify("act1_scene1", 0)
        
def on_escape_press():
    myscene.handler.notify("title_screen", False)
