import math

class Interpolator(object):
    def __init__(self, host_object, attr_name, end, start=None, 
                 name="value", speed=0.0, duration=0.0,
                 done_function=None):
        self.host_object = host_object
        self.attr_name = attr_name
        self.done_function = done_function
        self.start = start
        if self.start is None:
            self.start = getattr(host_object, attr_name)
        self.end = end
        self.name = name
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
    
    def __repr__(self):
        fmt = "Interpolator '%s' on %s.%s from %0.2f to %0.2f taking %0.2f seconds)"
        return fmt % (self.name, str(self.host_object), self.attr_name, 
                      self.start, self.end, self.duration)
    

class LinearInterpolator(Interpolator):
    def __init__(self, *args, **kwargs):
        super(LinearInterpolator, self).__init__(*args, **kwargs)
        self.update(0.0)
    
    def update(self, dt=0):
        self.progress += dt
        setattr(self.host_object, self.attr_name, self.start + self.progress*self.speed)
    
    def __repr__(self):
        fmt = "LinearInterpolator '%s' on %s.%s from %0.2f to %0.2f taking %0.2f seconds)"
        return fmt % (self.name, str(self.host_object), self.attr_name, 
                      self.start, self.end, self.duration)
    

class Linear2DInterpolator(Interpolator):
    def __init__(self, host_object, attr_name, end_tuple, name="position", 
                 start_tuple=None, speed=0.0, duration=0.0, done_function=None):
        if start_tuple is None:
            start_tuple = getattr(host_object, attr_name)
        self.start_tuple = start_tuple
        self.end_tuple = end_tuple
        
        self.speed = speed
        self.duration = duration
        
        diff_tuple = (end_tuple[0] - start_tuple[0], end_tuple[1] - start_tuple[1])
        angle = math.atan2(diff_tuple[1], diff_tuple[0])
        length = math.sqrt(diff_tuple[0] * diff_tuple[0] + diff_tuple[1] * diff_tuple[1])
        
        super(Linear2DInterpolator, self).__init__(host_object, attr_name, 
                                                   end=length, start=0.0, 
                                                   speed=self.speed, 
                                                   name=name, done_function=done_function,
                                                   duration=self.duration)
        
        self.x_speed = self.speed*math.cos(angle)
        self.y_speed = self.speed*math.sin(angle)
        
        self.update(0.0)
    
    def update(self, dt=0):
        super(Linear2DInterpolator, self).update(dt)
        new_tuple = ((self.start_tuple[0] + self.progress*self.x_speed),
                     (self.start_tuple[1] + self.progress*self.y_speed))
        setattr(self.host_object, self.attr_name, new_tuple)
    
    def __repr__(self):
        fmt = "Linear2DInterpolator '%s' on %s.%s from %s to %s taking %0.2f seconds)"
        return fmt % (self.name, str(self.host_object), self.attr_name, 
                      str(self.start_tuple), str(self.end_tuple), self.duration)
    

