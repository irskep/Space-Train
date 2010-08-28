import pyglet, math

main_window = None
norm_w = 1024
norm_h = 768
scale_factor = 1.0
scripts_enabled = True
sidebar_w = 0

camera_x = 0
camera_y = 0
camera_target_x = 0
camera_target_y = 0
camera_speed = 1000

camera_min = (norm_w//2, norm_h//2)
camera_max = (norm_w, norm_h)

keys = None

def init_keys():
    global keys
    keys = pyglet.window.key.KeyStateHandler()
    main_window.push_handlers(keys)

def init_scale():
    global norm_w, norm_h, scale_factor, camera_min, camera_max
    scale_factor_1 = main_window.height / float(norm_h)
    norm_w_1 = int(main_window.width/scale_factor_1)
    scale_factor_2 = main_window.width / float(norm_w)
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

def move_camera(dt):
    global camera_x, camera_y
    move_amt = camera_speed*dt
    if camera_x < camera_target_x-move_amt: camera_x += move_amt
    if camera_x > camera_target_x+move_amt: camera_x -= move_amt
    if abs(camera_x-camera_target_x) <= move_amt: camera_x = camera_target_x
    if camera_y < camera_target_y-move_amt: camera_y += move_amt
    if camera_y > camera_target_y+move_amt: camera_y -= move_amt
    if abs(camera_y-camera_target_y) <= move_amt: camera_y = camera_target_y
    camera_x = min(max(camera_x, camera_min[0]), camera_max[0])
    camera_y = min(max(camera_y, camera_min[1]), camera_max[1])

def scale():
    pyglet.gl.glScalef(scale_factor,scale_factor,1)

def apply_camera():
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(-camera_x+norm_w//2+sidebar_w, -camera_y+norm_h//2,0)

def unapply_camera():
    pyglet.gl.glPopMatrix()

def mouse_to_canvas(x, y):
    return ((camera_x-norm_w//2 + x - sidebar_w)/scale_factor + (camera_x - norm_w/2)*(1.0-1.0/scale_factor), 
            (camera_y-norm_h//2 + y)/scale_factor + (camera_y - norm_h/2)*(1.0-1.0/scale_factor))
