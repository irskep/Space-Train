import pyglet, functools, json, os, random

# Easy access if you just import util
import const
import dijkstra
import draw
import settings
import vector
import walkpath

# Intercept resource loads

print_loads = True

preload = [
'actors/inga/stand_right.png',
'actors/femtourist/stand_front.png',
'actors/inga/talk_right_1.png',
'actors/femtourist/walk_left_1.png',
'environments/act1_scene1/1_0.png',
'actors/inga/talk_left_2.png',
'ui/purseopen.png',
'actors/seat/chair_left.png',
'environments/act1_scene1/overlay_0_0.png',
'actors/monitor/TV_Propaganda_8.png',
'actors/femtourist/walk_right_1.png',
'actors/monitor/StaticTV_1.png',
'actors/inga/talk_left_1.png',
'actors/femtourist/walk_right_3.png',
'actors/femtourist/walk_right_2.png',
'environments/act1_scene1/2_0.png',
'environments/transitions/test.png',
'actors/monitor/TV_Propaganda_6.png',
'actors/inga/talk_right_2.png',
'environments/act1_scene1/0_0.png',
'actors/monitor/TV_Propaganda_1.png',
'actors/monitor/TV_Propaganda_2.png',
'actors/femtourist/walk_right_4.png',
'actors/outlet_wire/outlet_wire.png',
'ui/purse.png',
'actors/seat/chair.png',
'actors/femtourist/walk_left_4.png',
'actors/inga/walk_left_1.png',
'actors/monitor/TV_Propaganda_5.png',
'actors/monitor/StaticTV_3.png',
'actors/shamus/shamus.png',
'actors/femtourist/walk_left_2.png',
'actors/inga/walk_right_1.png',
'actors/cart_lady/stand_right.png',
'actors/femtourist/walk_left_3.png',
'actors/monitor/StaticTV_4.png',
'actors/inga/walk_right_2.png',
'actors/monitor/TV_Propaganda_4.png',
'actors/intro_billboards/note.png',
'actors/luggage/luggage2.png',
'actors/inga/stand_front.png',
'actors/monitor/StaticTV_2.png',
'environments/act1_scene1/overlay_2_0.png',
'environments/the_vast_emptiness_of_space/0_0.png',
'actors/inga/sit.png',
'actors/tourist/stand_front.png',
'actors/monitor/TV_Propaganda_3.png',
'actors/conspiracy_theorist/conspiracytheorist.png',
'actors/monitor/TV_Propaganda_7.png',
'actors/intro_billboards/zeppelin.png',
'actors/seat/couch.png',
'environments/spacebackground.png',
'actors/inga/walk_left_2.png',
'actors/luggage/luggage.png',
'actors/inga/stand_left.png',
'ui/purse.png',
'ui/purseopen.png',
'environments/transitions/test.png',
'environments/act1_scene1/0_0.png',
'environments/act1_scene1/1_0.png',
'environments/act1_scene1/2_0.png',
'environments/act1_scene1/overlay_0_0.png',
'environments/act1_scene1/overlay_2_0.png',
'environments/spacebackground.png',
'actors/seat/chair.png',
'actors/seat/chair_left.png',
'actors/seat/couch.png',
'actors/thermostat/rising_1.png',
'actors/thermostat/rising_2.png',
'actors/thermostat/rising_3.png',
'actors/thermostat/rising_4.png',
'actors/thermostat/rising_5.png',
'actors/thermostat/rising_6.png',
'actors/thermostat/thermostat_1.png',
'actors/thermostat/thermostat_2.png',
'actors/thermostat/thermostat_3.png',
'actors/thermostat/thermostat_4.png',
'actors/luggage/luggage2.png',
'actors/luggage/luggage.png',
'actors/cart_lady/stand_right.png',
'actors/cart_lady/walk_right_1.png',
'actors/cart_lady/walk_right_2.png',
'actors/cart_lady/walk_left_1.png',
'actors/cart_lady/walk_left_2.png',
'actors/cart_lady/talk_right_1.png',
'actors/cart_lady/talk_right_2.png',
'actors/conspiracy_theorist/conspiracytheorist.png',
'actors/tourist/stand_front.png',
'actors/inga/stand_left.png',
'actors/inga/walk_left_1.png',
'actors/inga/walk_left_2.png',
'actors/inga/sit.png',
'actors/inga/talk_right_1.png',
'actors/inga/talk_right_2.png',
'actors/inga/talk_sit_left_1.png',
'actors/inga/talk_sit_left_2.png',
'actors/inga/walk_right_1.png',
'actors/inga/walk_right_2.png',
'actors/inga/stand_right.png',
'actors/inga/talk_left_1.png',
'actors/inga/talk_left_2.png',
'actors/inga/sit_left.png',
'actors/inga/stand_front.png',
'actors/femtourist/walk_right_1.png',
'actors/femtourist/walk_right_2.png',
'actors/femtourist/walk_right_3.png',
'actors/femtourist/walk_right_4.png',
'actors/femtourist/stand_front.png',
'actors/femtourist/walk_left_1.png',
'actors/femtourist/walk_left_2.png',
'actors/femtourist/walk_left_3.png',
'actors/femtourist/walk_left_4.png',
'actors/sneelock/stand_right.png',
'actors/sneelock/walk_right_1.png',
'actors/sneelock/walk_right_2.png',
'actors/sneelock/walk_right_3.png',
'actors/sneelock/stand_front.png',
'actors/sneelock/walk_left_1.png',
'actors/sneelock/walk_left_2.png',
'actors/sneelock/walk_left_3.png',
'actors/sneelock/stand_left.png',
'actors/monitor/StaticTV_1.png',
'actors/monitor/StaticTV_2.png',
'actors/monitor/StaticTV_3.png',
'actors/monitor/StaticTV_4.png',
'actors/monitor/TV_Propaganda_1.png',
'actors/monitor/TV_Propaganda_2.png',
'actors/monitor/TV_Propaganda_3.png',
'actors/monitor/TV_Propaganda_4.png',
'actors/monitor/TV_Propaganda_5.png',
'actors/monitor/TV_Propaganda_6.png',
'actors/monitor/TV_Propaganda_7.png',
'actors/monitor/TV_Propaganda_8.png',
'actors/outlet_wire/outlet_wire.png',
'actors/shamus/shamus.png',
'actors/shamus/eating_1.png',
'actors/shamus/eating_2.png',
'actors/shamus/eating_3.png',
'actors/space_bucks/five.png',
'actors/pen/pen.png',
'actors/notepad/notepad.png',
'actors/tasty_nuts/tasty_nuts.png',
'actors/lemonade/lemonade.png',
]

# preload = []

random.shuffle(preload)

def load_image(img):
    i = pyglet.resource.image(img)
    if print_loads:
        print "'%s'," % img
    return i

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
