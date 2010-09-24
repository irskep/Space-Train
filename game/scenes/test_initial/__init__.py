from engine import actor

# myscene is set by scene.py
myscene = None

def init():
    print "Initializing script for", myscene
    print "Not changing anything, accepting defaults"

def handle_event(event, *args):
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
    if clicked_actor.name == "another_fist":
        print "Initiating scene transfer."
        myscene.handler.notify("test_2")
    else:
        clicked_actor.prepare_jump()
        clicked_actor.next_action()
