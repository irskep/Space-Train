from engine import actor

myscene = None

def init():
    print "Initializing script for", myscene
    print "Not changing anything, accepting defaults"

def handle_event(event, *args):
    print "Handled", event, "with", args
