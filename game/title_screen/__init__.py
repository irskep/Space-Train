from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator

# myscene is set by scene.py
myscene = None

def init(fresh=True):
    myscene.ui.inventory.visible = False
    title = myscene.actors['go']
    title.use_mask_to_detect_clicks = False
    interp = PulseInterpolator(title.sprite, 'scale', 0.9, 1.0, speed=4)
    myscene.add_interpolator(interp)

def handle_event(event, *args):
    pass

def next(*args, **kwargs):
    myscene.handler.notify("intro", 0)  # magic numbers ftw

def actor_clicked(clicked_actor):
    if clicked_actor.identifier == "go":
        myscene.play_sound("new_game")
        interp = LinearInterpolator(myscene.actors['go'].sprite, 'scale', end=3.0, duration=0.72)
        myscene.add_interpolator(interp)
        interp = LinearInterpolator(myscene.actors['go'].sprite, 'opacity', 0.0, 
                     duration=0.72, done_function=next)
        myscene.add_interpolator(interp)
        interp = LinearInterpolator(myscene.actors['logo'].sprite, 'opacity', 0.0, 
                     duration=0.72)
        myscene.add_interpolator(interp)
