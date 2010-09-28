from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

# myscene is set by scene.py
myscene = None

def init():
    cart_lady = myscene.actors['cart_lady']
    cart_lady.prepare_walkpath_move('cart_lady_right')
    cart_lady.next_action()

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if info['actor'].identifier == 'cart_lady':
            if point == 'cart_lady_left':
                print "Send 'er to the right!"
                actor.prepare_walkpath_move('cart_lady_right')
            elif point == 'cart_lady_right':
                print "Send 'er back left!"
                actor.prepare_walkpath_move('cart_lady_left')
            else:
                print 'unknown cart lady event info', info
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):
    print "Clicked on %s" % clicked_actor.name
