import pyglet, functools

import gamestate

class apply_camera(object):
    def __init__(self, c):
        self.camera = c
    
    def __enter__(self):
        self.camera.apply()
    
    def __exit__(self, type, value, traceback):
        self.camera.unapply()
    

class CameraPoint(object):
    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position
    

class Camera(object):
    def __init__(self, min_bounds=None, max_bounds=None, speed=50000.0, dict_repr=None):
        self.min_bounds = min_bounds or gamestate.camera_min
        self.max_bounds = max_bounds or gamestate.camera_max
        self._x, self._y = self.min_bounds
        dict_repr = dict_repr or {}
        self.points = {identifier: CameraPoint(identifier, (d['x'], d['y'])) \
                       for identifier, d in dict_repr.viewitems()}
    
    def _set_position(self, p):
        self._x, self._y = self.constrain_point(*p)
    
    position = property(lambda self: (self._x, self._y), _set_position)
    
    def dict_repr(self):
        return {identifier: {'x': p.position[0], 
                             'y': p.position[1]} 
                for identifier, p in self.points.viewitems()}
    
    def constrain_point(self, x, y):
        x = min(max(x, self.min_bounds[0]), self.max_bounds[0])
        y = min(max(y, self.min_bounds[1]), self.max_bounds[1])
        return (x, y)
    
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
    
    def apply(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(-self.position[0]+gamestate.norm_w//2, 
                               -self.position[1]+gamestate.norm_h//2,0)
    
    def unapply(self):
        pyglet.gl.glPopMatrix()
    
    def mouse_to_canvas(self, x, y):
        return (x/gamestate.scale_factor + self.position[0]-gamestate.norm_w//2, 
                y/gamestate.scale_factor + self.position[1]-gamestate.norm_h//2)

    # returns a position on the screen based on a point in the game world (i.e. where a point is relative to the camera)
    def world_to_screen_position(self, x, y):
        return ( (x/gamestate.scale_factor) - (self.position[0]-gamestate.norm_w//2), 
                (y/gamestate.scale_factor) - (self.position[1]-gamestate.norm_h//2))
    
