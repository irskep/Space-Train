import game_state

class SceneHandler(object):
    def __init__(self, scene_object, environment_object):
        self.scene = scene_object
        self.environment = environment_object
        self.main_actor = None
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.main_actor:
            self.main_actor.move_to(x, y)
    
    def __repr__(self):
        return "SceneHandler(scene_object=%s, environment_object=%s)" % (str(self.scene), str(self.environment))