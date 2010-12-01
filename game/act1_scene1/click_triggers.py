from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamehandler
from engine import gamestate
from engine import convo
from engine import util

def inga_walk(actor, point):
    global do_sit
    global sneelock_distracted
    if point == "inga_attempt_silver_class":
        if not sneelock_distracted:
            sneelock = myscene.actors['sneelock']
            sneelock.prepare_walkpath_move("sneelock_block")
            sneelock.next_action()
            myscene.convo.begin_conversation("you_shall_not_pass")
    if point == "transition_left":
        myscene.handler.notify("act1_scene2")
    if re.match(r"seat_\d+", point) and do_sit:
        myscene.actors['main'].update_state("sit")
        do_sit = False

def levity_walk(actor, point):
    print "Walk handler called..."
    global levity_exposition            #gross how can we un-global this? (i.e. static local var in C)
    global levity_direction
    levity = myscene.actors['levity']
    next_point = point
    if point == "levity_left" or point == "levity_right":   
        if point == "levity_left":
            levity_direction = "right"
            next_point = "levity_1"
        elif point == "levity_right":
            levity_direction = "left"
            next_point = "levity_4"
        #levity.prepare_walkpath_move(next_point)
        pyglet.clock.schedule_once(util.make_dt_wrapper(levity.prepare_walkpath_move), 1, next_point)
        pyglet.clock.schedule_once(levity.next_action, 60)
        
    else:
        if point == "levity_1":
            next_point = "levity_2" if levity_direction == "right" else "levity_left"
        elif point == "levity_2":
            next_point = "levity_3" if levity_direction == "right" else "levity_1"
        elif point == "levity_3":
            next_point = "levity_4" if levity_direction == "right" else "levity_2"
        elif point == "levity_4":
            if levity_exposition is False:
                levity_exposition = True
                #begin convo
                actor.update_state("stand_right")
                myscene.begin_conversation("introduction")
            else:
                next_point = "levity_right" if levity_direction == "right" else "levity_3"
        
        if next_point is not point:    
            levity.prepare_walkpath_move(next_point)
            print "Moving from %s to %s..." % (point, next_point)

def tourist_walk(actor, point):
    global sneelock_distracted
    if point == "tourist_complain":
        sneelock_distracted = True
        myscene.begin_background_conversation("its_too_hot")
        
def sneelock_walk(actor, point):
    if point == "sneelock_inspect":
        pyglet.clock.schedule_once(util.make_dt_wrapper(myscene.begin_background_conversation), 5, "sneelock_checks_it_out")
    
def potato_roll(actor, point):
    point_match = re.search(r"potato_(\d+)", point)
    if point_match and not myscene.handler.handler.game_variables['potato_stop']:
        current_index = int(point_match.group(1))
        next_index = current_index + 1
        if next_index > 40:
            next_index = 1
        next_point = "potato_%d" % next_index
        print "Potato rolling from %s to %s" % (point, next_point)
        #actor.prepare_walkpath_move(next_point)
        pyglet.clock.schedule_once(util.make_dt_wrapper(actor.prepare_walkpath_move), 0, next_point)
        #actor.next_action()
        pyglet.clock.schedule_once(util.make_dt_wrapper(actor.next_action), 0)
