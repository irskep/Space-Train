import math, operator, functools

def round_down(v):
    """Round down both values of a 2-tuple to integers"""
    return (int(v[0]), int(v[1]))

def tuple_op(a, b, op=operator.sub):
    """Apply op() to respective coordinates of two 2-tuples"""
    return (op(a[0], b[0]), op(a[1], b[1]))

def length(v):
    """Get the length of a 2D vector"""
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def length_squared(v):
    """Get the squared length of a 2D vector"""
    return v[0]*v[0] + v[1]*v[1]
    
def intersects(x, y, box_x, box_y, box_w, box_h):
    return (x > box_x and x < box_x + box_w and
            y > box_y and y < box_y + box_y)

def op_between(func):
    """Apply a vector operaton on the vector between two 2D points"""
    def f(a, b):
        return func(tuple_op(a, b, operator.sub))
    return f

# Find distance or squared distance (faster) between two 2D points
dist_between = op_between(length)
dist_squared_between = op_between(length_squared)

def normalize(v):
    """Normalize a 2D vector"""
    l = length(v)
    return (v[0]/l, v[1]/l)

def dot(x, y):
    """Dot product of a vector"""
    return x[0]*y[0] + x[1]*y[1]

def scalar_mult(v, t):
    """Multiply both values of a 2D vector by a scalar"""
    return (v[0]*t, v[1]*t)

def closest_point_on_line(point, a, b):
    """Find the closest point on a line between (a) and (b) to (point)"""
    # Shamelessly stolen from the internet and ported to Python
    # http://www.gamedev.net/community/forums/topic.asp?topic_id=198199
    
    c = tuple_op(point, a, operator.sub)        # Vector from a to Point
    v = normalize(tuple_op(b, a, operator.sub)) # Unit Vector from a to b
    d = length(tuple_op(b, a, operator.sub))    # Length of the line segment
    t = dot(v, c)                               # Intersection point Distance from a
    
    # Check to see if the point is on the line
    # if not then return the endpoint
    if t < 0: 
        return a
    if t > d: 
        return b
    
    # get the distance to move from point a
    v = scalar_mult(v, t)
    
    # move from point a to the nearest point on the segment
    return tuple_op(a, v, operator.add)
