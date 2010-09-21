import pyglet, functools

# Easy access if you just import util
import dijkstra
import draw
import settings
import vector
import walkpath

# Functional

def first(list_to_search, condition_to_satisfy):
    """Return first item in a list for which condition_to_satisfy(item) returns True"""
    for item in list_to_search:
        if condition_to_satisfy(item):
            return item
    return None

# Conventions

def respath(*args):
    return '/'.join(args)

def respath_func_with_base_path(*args):
    return functools.partial(respath, *args)

class ClipGroup(pyglet.graphics.OrderedGroup): 
    """Sprite group that clips to a rectangle"""
    def __init__(self, name="ClipGroup", order=0, parent=None): 
        super(ClipGroup, self).__init__(order, parent) 
        self.x, self.y, self.w, self.h = 0, 0, 256, 256 
        self.name=name 
    
    def set_state(self): 
        gl.glScissor(self.x, self.y, self.w, self.h) 
        gl.glEnable(gl.GL_SCISSOR_TEST) 
    
    def unset_state(self): 
        gl.glDisable(gl.GL_SCISSOR_TEST)