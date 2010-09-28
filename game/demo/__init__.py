import functools

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

# myscene is set by scene.py
myscene = None

def init():
    cart_lady = myscene.actors['cart_lady']
    cart_lady.prepare_walkpath_move('cart_lady_right')
    cart_lady.next_action()

def cart_lady_walk(actor, point):
    if point == 'cart_lady_left':
        actor.prepare_walkpath_move('cart_lady_right')
    elif point == 'cart_lady_right':
        actor.prepare_walkpath_move('cart_lady_left')
    else:
        print 'unknown cart lady event'

def inga_walk(actor, point):
    if point == 'inga_walk_middle':
        myscene.begin_conversation('beans_1')
        bean_salesman = myscene.actors['bean_salesman']

def end_conversation(convo_name):
    if convo_name == 'beans_1':
        bean_salesman = myscene.actors['bean_salesman']
        bean_salesman.jump()
        myscene.begin_conversation('beans_2')
    elif convo_name == 'beans_2':
        myscene.actors['main'].update_state('stand_front')

walk_handlers = {
    'cart_lady': cart_lady_walk,
    'main': inga_walk
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
