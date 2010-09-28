import pyglet, functools

import gamestate

class CameraPoint(object):
    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position
    

class Camera(object):
    def __init__(self, min_bounds=None, max_bounds=None, speed=50000.0, dict_repr=None):
        self.min_bounds = min_bounds or gamestate.camera_min
        self.max_bounds = max_bounds or gamestate.camera_max
        self.speed = speed
        self.position = self.min_bounds
        self.target = self.position
        dict_repr = dict_repr or {}
        self.points = {identifier: CameraPoint(identifier, (d['x'], d['y'])) \
                       for identifier, d in dict_repr.viewitems()}
    
    def dict_repr(self):
        return {identifier: {'x': p.position[0], 
                             'y': p.position[1]} 
                for identifier, p in self.points.viewitems()}
    
    def constrain_point(self, x, y):
        x = min(max(x, self.min_bounds[0]), self.max_bounds[0])
        y = min(max(y, self.min_bounds[1]), self.max_bounds[1])
        return (x, y)
    
    def set_target(self, x, y):
        self.target = self.constrain_point(x, y)
    
    def set_position(self, x, y):
        self.position = self.constrain_point(x, y)
        self.target = self.position
    
    def camera_point_near_point(self, mouse):
        close = lambda a, b: abs(a-b) <= 5
        for point in self.points.viewvalues():
            if close(point.position[0], mouse[0]) and close(point.position[1], mouse[1]):
                return point
        return None
    
    def add_point(self, x, y, identifier=None):
        if identifier is None:
            next_identifier = 1
            while self.points.has_key("camera_point_%d" % next_identifier):
                next_identifier += 1
            identifier = "camera_point_%d" % next_identifier
        self.points[identifier] = CameraPoint(identifier, self.constrain_point(x, y))
        return self.points[identifier]
    
    def remove_point(self, point):
        if hasattr(point, 'identifier'):
            identifier = point.identifier
        else:
            # We were probably passed the identifier string
            identifier = point
        try:
            del self.points[identifier]
        except KeyError:
            return
    
    def update(self, dt):
        move_amt = self.speed*dt
        x, y = self.position
        tx, ty = self.target
        if x < x - move_amt: x += move_amt
        if x > tx + move_amt: x -= move_amt
        if abs(x - tx) <= move_amt: x = tx
        if y < ty - move_amt: y += move_amt
        if y > ty + move_amt: y -= move_amt
        if abs(y - ty) <= move_amt: y = ty
        self.position = self.constrain_point(x, y)
    
    def apply(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-self.position[0]+gamestate.norm_w//2, 
                               -self.position[1]+gamestate.norm_h//2,0)
    
    def unapply(self):
        pyglet.gl.glPopMatrix()
    
    def mouse_to_canvas(self, x, y):
        return (x/gamestate.scale_factor + self.position[0]-gamestate.norm_w//2, 
                y/gamestate.scale_factor + self.position[1]-gamestate.norm_h//2)
    

def obey_camera(draw_function):
    @functools.wraps(draw_function)
    def draw_with_camera(*args, **kwargs):
        # args[0] is the class instance
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-args[0].camera.position[0]+gamestate.norm_w//2, 
                               -args[0].camera.position[1]+gamestate.norm_h//2,0)
        draw_function(*args, **kwargs)
        pyglet.gl.glPopMatrix()
    return draw_with_camera
