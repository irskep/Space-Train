from engine import actor, scenehandler

class TestSceneHandler(scenehandler.SceneHandler):
    def __init__(self, *args):
        super(TestSceneHandler, self).__init__(*args)
        self.main_actor = actor.Actor('fist', self.scene, batch=self.scene.batch, x=300, y=300)
    

scene_handler = None

def init(scene_obj, env):
    global scene_handler
    scene_handler = TestSceneHandler(scene_obj, env)
    print scene_handler
