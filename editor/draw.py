import math
import pyglet.graphics, pyglet.image, pyglet.gl

grid_spacing = 50

def set_color(r=0.0, g=0.0, b=0.0, a=1.0, color=None):
    if color is not None: pyglet.gl.glColor4f(*color)
    else: pyglet.gl.glColor4f(r,g,b,a)

def image(img, x, y):
    img.blit(x,y)

def label(label):
    """Draws a Pyglet label."""
    label.draw()

def line(x1, y1, x2, y2, colors=None):
    if colors is None:
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)))
    else:
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1, x2, y2)), ('c4f', colors))

def line_loop(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors is None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP,('v2f', points),('c4f', colors))

def rect(x1, y1, x2, y2):
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

def rect_outline(x1, y1, x2, y2):
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

def _concat(it):
    return list(y for x in it for y in x)

def _iter_ellipse(x1, y1, x2, y2, da=None, step=None, dashed=False):
    xrad = abs((x2-x1) / 2.0)
    yrad = abs((y2-y1) / 2.0)
    x = (x1+x2) / 2.0
    y = (y1+y2) / 2.0
    
    if da and step:
        raise ValueError("Can only set one of da and step")
    
    if not da and not step:
        step = 8.0
    
    if not da:
        # use the average of the radii to compute the angle step
        # shoot for segments that are 8 pixels long
        step = 32.0
        rad = max((xrad+yrad)/2, 0.01)
        rad_ = max(min(step / rad / 2.0, 1), -1)
        
        # but if the circle is too small, that would be ridiculous
        # use pi/16 instead.
        da = min(2 * math.asin(rad_), math.pi / 16)
    
    a = 0.0
    while a <= math.pi * 2:
        yield (x + math.cos(a) * xrad, y + math.sin(a) * yrad)
        a += da
        if dashed: a += da

def ellipse(x1, y1, x2, y2):
    points = _concat(_iter_ellipse(x1, y1, x2, y2))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

def ellipse_outline(x1, y1, x2, y2):
    points = _concat(_iter_ellipse(x1, y1, x2, y2))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP, ('v2f', points))

def circle(x, y, rad):
    ellipse_outline(x-rad, y-rad, x+rad, y+rad)

def circle_outline(x, y, rad):
    ellipse_outline(x-rad, y-rad, x+rad, y+rad)

def _iter_ngon(x, y, r, sides, start_angle = 0.0):
    rad = max(r, 0.01)
    rad_ = max(min(sides / rad / 2.0, 1), -1)
    da = math.pi * 2 / sides
    a = start_angle
    while a <= math.pi * 2 + start_angle:
        yield (x + math.cos(a) * r, y + math.sin(a) * r)
        a += da

def ngon(x, y, r, sides, start_angle = 0.0):
    points = _concat(_iter_ngon(x, y, r, sides, start_angle))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_TRIANGLE_FAN, ('v2f', points))

def ngon_outline(x, y, r, sides, start_angle = 0.0):
    points = _concat(_iter_ngon(x, y, r, sides, start_angle))
    pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_LINE_LOOP, ('v2f', points))

def points(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points),('c4f', colors))

def polygon(points, colors=None):
    """
    @param points: A list formatted like [x1, y1, x2, y2...]
    @param colors: A list formatted like [r1, g1, b1, a1, r2, g2, b2 a2...]
    """
    if colors == None:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POLYGON,('v2f', points),('c4f', colors))

def quad(points,colors=None):
    if colors == None:
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', points))
    else:
        pyglet.graphics.draw(len(points)/2, pyglet.gl.GL_POINTS,('v2f', points),('c4f', colors))

def grid(x, y, width, height):
    x_start, y_start = x, y
    x_end, y_end = x + width, y + height
    x -= x % grid_spacing
    y -= y % grid_spacing
    while x < x_end:
        line(x,y,x,y+height)
        x += grid_spacing
    x = x_start
    while y < y_end:
        line(x,y,x+width,y)
        y += grid_spacing
