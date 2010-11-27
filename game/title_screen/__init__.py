from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator

# myscene is set by scene.py
myscene = None

def init(fresh=True):
    myscene.ui.inventory.visible = False
    title = myscene.actors['go']
    interp = PulseInterpolator(title.sprite, 'scale', 0.9, 1.0, speed=4)
    myscene.add_interpolator(interp)

def handle_event(event, *args):
    pass

def actor_clicked(clicked_actor):
    if clicked_actor.identifier == "go":
        myscene.handler.notify("intro")
        interp = LinearInterpolator(clicked_actor.sprite, 'rotation', 0.0, 360, speed=500.0)
        myscene.add_interpolator(interp)
