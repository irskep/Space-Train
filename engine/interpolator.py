import math

class Interpolator(object):
    def __init__(self, host_object, attr_name, end, start=None, speed=0.0, duration=0.0):
        self.host_object = host_object
        self.attr_name = attr_name
        self.start = start
        if self.start is None:
            self.start = getattr(host_object, attr_name)
        self.end = end
        self.speed = speed
        self.duration = duration
        self.fix_speed_and_duration()
        self.progress = 0.0
        self.complete = lambda: abs(self.progress) >= self.duration
    
    def fix_speed_and_duration(self):
        if self.speed == 0.0:
            if self.duration == 0.0:
                self.speed = 100.0
                self.duration = abs((self.start-self.end)/self.speed)
            else:
                self.speed = abs((self.start-self.end)/self.duration)
        elif self.duration == 0.0:
            self.duration = abs((self.start-self.end)/self.speed)
        if self.end < self.start:
            self.speed = -self.speed
    
    def update(self, dt=0):
        self.progress += dt
    

class LinearInterpolator(Interpolator):
    def __init__(self, *args):
        super(LinearInterpolator, self).__init__(*args)
        self.update(0.0)
    
    def update(self, dt=0):
        self.progress += dt
        setattr(self.host_object, self.attr_name, self.start + self.progress*self.speed)
    

class PositionInterpolator(Interpolator):
    def __init__(self, host_object, attr_name, end_tuple, start_tuple=None, speed=0.0, duration=0.0):
        if start_tuple is None:
            start_tuple = getattr(host_object, attr_name)
        self.start_tuple = start_tuple
        self.end_tuple = end_tuple
        
        self.speed = speed
        self.duration = duration
        
        diff_tuple = (start_tuple[0] - end_tuple[0], start_tuple[1] - end_tuple[1])
        angle = math.atan2(diff_tuple[1], diff_tuple[0])
        length = math.sqrt(diff_tuple[0] * diff_tuple[0] + diff_tuple[1] * diff_tuple[1])
        
        super(PositionInterpolator, self).__init__(host_object, attr_name, 0.0, length, self.speed, self.duration)
        
        self.x_speed = self.speed*math.cos(angle)
        self.y_speed = self.speed*math.sin(angle)
        
        self.update(0.0)
    
    def update(self, dt=0):
        super(PositionInterpolator, self).update(dt)
        new_tuple = ((self.start_tuple[0] + self.progress*self.x_speed),
                     (self.start_tuple[1] + self.progress*self.y_speed))
        setattr(self.host_object, self.attr_name, new_tuple)
    
    def __repr__(self):
        fmt = "PositionInterpolator(host_object='%s', attr_name='%s', start_tuple='%s', end_tuple='%s', duration=%d)"
        return fmt % (str(self.host_object), str(self.attr_name), 
                      str(self.start_tuple), str(self.end_tuple), self.duration)
    

