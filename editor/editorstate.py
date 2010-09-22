import pyglet
from engine import gamestate

status_label = None

def init():
    global status_label

    l = pyglet.text.Label('', x=gamestate.main_window.width, 
                              y=gamestate.main_window.height, 
                              font_name = "Courier New",
                              font_size = 12,
                              color = (0,0,0,255),
                              anchor_x='right', anchor_y='top')
    status_label = l

def set_status_message(message=''):
    status_label.begin_update()
    status_label.text = message
    status_label.end_update()
