import pyglet, math, functools

main_window = None
norm_w = 1360
norm_h = 768
scale_factor = 1.0
scripts_enabled = True

camera_min = (norm_w//2, norm_h//2)
camera_max = (norm_w, norm_h)

keys = None

def init_keys():
    global keys
    keys = pyglet.window.key.KeyStateHandler()
    main_window.push_handlers(keys)

def init_scale():
    global norm_w, norm_h, scale_factor, camera_min, camera_max
    if not main_window.fullscreen:
        scale_factor = 1.0
        norm_w = main_window.width
        norm_h = main_window.height
    else:
        scale_factor_1 = main_window.height / float(norm_h)
        scale_factor_2 = main_window.width / float(norm_w)
        norm_w_1 = int(main_window.width/scale_factor_1)
        norm_h_2 = int(main_window.height/scale_factor_1)
        if scale_factor_2 < scale_factor_1:
            norm_h = norm_h_2
            scale_factor = scale_factor_2
        else:    
            norm_w = norm_w_1
            scale_factor = scale_factor_1
    norm_theta = math.atan2(norm_h, norm_w)
    camera_min = (norm_w//2, norm_h//2)
    camera_max = (norm_w, norm_h)

def scale():
    pyglet.gl.glScalef(scale_factor,scale_factor,1)

def scaled(draw_function):
    """Decorator to cause a drawing function to be scaled by scale_factor"""
    if scale_factor == 1.0:
        return draw_function
    else:
        @functools.wraps(draw_function)
        def draw_scaled(*args, **kwargs):
            pyglet.gl.glPushMatrix()
            pyglet.gl.glScalef(scale_factor,scale_factor,1)
            draw_function(*args, **kwargs)
            pyglet.gl.glPopMatrix()
        return draw_scaled
