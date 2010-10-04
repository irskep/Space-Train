from engine import actor

# myscene is set by scene.py
myscene = None

def init():
    print "Initializing script for", myscene
    print "Not changing anything, accepting defaults"

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    clicked_actor.prepare_jump()
    clicked_actor.next_action()

def transition_from(last_scene):
    print "transitioned from", last_scene
