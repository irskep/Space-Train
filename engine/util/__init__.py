import pyglet, functools, json, os

# Easy access if you just import util
import const
import dijkstra
import draw
import settings
import vector
import walkpath

# Intercept resource loads

print_loads = False

preload = [
'ui/purse.png',
'ui/purseopen.png',
'actors/fist/stand_front.png',
'environments/transitions/test.png',
'environments/act1_scene1/0_0.png',
'environments/act1_scene1/1_0.png',
'environments/act1_scene1/2_0.png',
'environments/act1_scene1/overlay_0_0.png',
'environments/act1_scene1/overlay_1_0.png',
'environments/act1_scene1/overlay_2_0.png',
'environments/spacebackground.png',
'actors/fist/climb_down.png',
'actors/fist/climb_up.png',
'actors/fist/walk_right_1.png',
'actors/fist/walk_right_2.png',
'actors/fist/walk_left_1.png',
'actors/fist/walk_left_2.png',
'actors/fist/walk_back_1.png',
'actors/fist/walk_back_2.png',
'actors/fist/walk_front_1.png',
'actors/fist/walk_front_2.png',
'actors/fist/stand_front.png',
'actors/seat/chair.png',
'actors/seat/couch.png',
'actors/thermostat/thermostat.png',
'actors/cart_lady/stand_right.png',
'actors/cart_lady/walk_right_1.png',
'actors/cart_lady/walk_right_2.png',
'actors/cart_lady/walk_left_1.png',
'actors/cart_lady/walk_left_2.png',
'actors/conspiracy_theorist/conspiracytheorist.png',
'actors/hipster_liam/hipster_liam.png',
'actors/inga/walk_right_1.png',
'actors/inga/walk_right_2.png',
'actors/inga/walk_left_1.png',
'actors/inga/walk_left_2.png',
'actors/inga/sit.png',
'actors/inga/stand_right.png',
'actors/inga/talk_right_1.png',
'actors/inga/talk_right_2.png',
'actors/inga/stand_front.png',
'actors/tourist/head.png',
'actors/hold_steady_fat_man/stand_front.png',
'actors/hipster_amanda/hipster_amanda.png',
'actors/hipster_fran/hipster_fran.png',
'actors/shamus/shamus.png',
'actors/space_bucks/five.png',
]

def load_image(img):
    if print_loads:
        print "'%s'," % img
    return pyglet.resource.image(img)

# Functional

def first(list_to_search, condition_to_satisfy):
    """Return first item in a list for which condition_to_satisfy(item) returns True"""
    for item in list_to_search:
        if condition_to_satisfy(item):
            return item
    return None

class pushmatrix(object):
    def __init__(self, gl_func, *args, **kwargs):
        super(pushmatrix, self).__init__()
        self.gl_func = gl_func
        self.args = args
        self.kwargs = kwargs
    
    def __enter__(self):
        pyglet.gl.glPushMatrix()
        self.gl_func(*self.args, **self.kwargs)
    
    def __exit__(self, type, value, traceback):
        pyglet.gl.glPopMatrix()
    

# Conventions

def respath(*args):
    return '/'.join(args)

def respath_func_with_base_path(*args):
    return functools.partial(respath, *args)

def mkdir_if_absent(path):
    if not os.path.exists(path):
        os.mkdir(path)

def load_json(path):
    with open('%s.json' % path, 'r') as f:
        return json.load(f)

def save_json(data, path):
    """Save data to path. Appends .json automatically."""
    with open("%s.json" % path, 'w') as f:
        json.dump(data, f, indent=4)

        
def make_dt_wrapper(func):
    @functools.wraps(func)
    def inner_func(dt, *args, **kwargs):
        func(*args, **kwargs)
    return inner_func
        
# Convenience and global use

def load_sprite(path, *args, **kwargs):
    loaded_image = load_image(respath(*path))
    return pyglet.sprite.Sprite(loaded_image, *args, **kwargs)

def image_alpha_at_point(img, x, y):
    x, y = int(x), int(y)
    pixel_data = img.get_image_data().get_data('RGBA',img.width*4)
    pos = y * img.width * 4 + x * 4
    
    if pos+3 < len(pixel_data):
        try:
            return pixel_data[pos+3]/255.0
        except TypeError:
            return ord(pixel_data[pos+3])/255.0
    else:
        return 0

# caution - broken. doesn't account for anchors
def intersects_sprite(x, y, sprite):
    return x > sprite.x and y > sprite.y and x < sprite.x + sprite.width and y < sprite.y + sprite.height
