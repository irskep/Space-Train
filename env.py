import pyglet, math

main_window = None
norm_w = 1024
norm_h = 768
scale_factor = 1.0

dt = 0.0

camera_x = 0
camera_y = 0
camera_target_x = 0
camera_target_y = 0
cvx = 1
cvy = 1

def init_scale():
    global norm_w, norm_h, scale_factor
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

def move_camera(x, y):
    global camera_x, camera_y
    if camera_x < camera_target_x-cvx: camera_x += cvx
    if camera_x > camera_target_x+cvx: camera_x -= cvx
    if abs(camera_x-camera_target_x) <= cvx: camera_x = camera_target_x
    if camera_y < camera_target_y-cvy: camera_y += cvy
    if camera_y > camera_target_y+cvy: camera_y -= cvy
    if abs(camera_y-camera_target_y) <= cvy: camera_y = camera_target_y

def scale():
    pyglet.gl.glScalef(scale_factor,scale_factor,1)

def apply_camera():
    pyglet.gl.glTranslatef( -camera_x+norm_w//2+sidebar_w//2, -camera_y+norm_h//2,0)
