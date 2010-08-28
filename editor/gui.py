"""
Buttons, etc.
"""

import pyglet, resources, graphics, draw, math
from settings import settings
from dialogs import *

class Button(object):
    """Basic button class. Ignore all methods except the constructor."""
    def __init__(self, image, action, x, y, text="", parent_group = None, more_draw = None):
        """
        @param image:   Button background image
        @param action:  Function to call when pressed
        @param x, y:    Bottom left corner position
        @param text:    Label text
        @param parent_group: L{ButtonGroup} that owns this object.
        @param more_draw: Function called immediately after the button is drawn. Use if you want to draw more stuff on top of the button other than an image. See L{tool.generate_brush_selector()} for an example.
        """
        self.action = action
        self.x, self.y = x, y
        self.selected = False
        self.pressed = False
        self.clicked_here = False
        self.image = image
        self.label = pyglet.text.Label(
            text, font_size=20, color=(0,0,0,255),
            x=self.x+self.image.width/2, y=self.y+self.image.height/2,
            anchor_x='center', anchor_y='center'
        )
        self.width = self.image.width
        self.height = self.image.height
        self.more_draw = more_draw
        self.parent_group = parent_group
        if self.parent_group != None: self.parent_group.add(self)
    
    def draw(self):
        """Internal use only."""
        color = (1,1,1,1)
        if self.parent_group != None and self.selected: color = (0.8, 0.8, 0.8, 1)
        if self.pressed: color = (0.7, 0.7, 0.7, 1)
        draw.set_color(color=color)
        draw.image(self.image,self.x,self.y)
        draw.set_color(1,1,1,1)
        draw.label(self.label)
        if self.more_draw != None: self.more_draw()
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Internal use only."""
        if self.clicked_here and self.coords_inside(x,y):
            self.pressed = True
            self.clicked_here = True
        else:
            self.pressed = False
        #self.on_mouse_press(x,y,None,None)
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Internal use only."""
        if self.coords_inside(x,y):
            self.pressed = True
            self.clicked_here = True
        else:
            self.pressed = False
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Internal use only."""
        if self.pressed and self.clicked_here:
            if self.parent_group != None: self.parent_group.select(self)
            self.action()
            self.pressed = False
        self.clicked_here = False
    
    def select(self):
        """
        After making a button group, call one button's select() method to make
        it the default. The button's action is not called.
        """
        if self.parent_group != None: self.parent_group.select(self)
    
    def coords_inside(self, x, y):
        """
        Check if (x,y) is inside the button.
        @rtype: boolean
        """
        return x >= self.x and y >= self.y and x <= self.x + self.width and y <= self.y + self.height
    

class Label(Button):
    def __init__(self, text, x, y, size=20):
        self.x, self.y = x, y
        self.selected = False
        self.pressed = False
        self.clicked_here = False
        self.label = pyglet.text.Label(text, font_size=size, color=(0,0,0,255),
                                        x=self.x, y=self.y,
                                        anchor_x='left', anchor_y='bottom')
        self.width = self.label.content_width
        self.height = self.label.content_height
        self.action = self.do_nothing
        self.draw = self.label.draw
        self.on_mouse_drag = self.do_nothing
        self.on_mouse_press = self.do_nothing
        self.on_mouse_release = self.do_nothing
        self.select = self.do_nothing
    
    def set_text(self, text):
        self.label.text = text.strip()
        self.width = self.label.content_width
        self.height = self.label.content_height
    
    def do_nothing(*args, **kwargs):
        pass

class ImageButton(Button):
    """
    Like Button, takes two images as arguments instead of more_draw. ImageButtons are much more common than regular Buttons in LevelEditor because the interface is almost entirely without text.
    
    Most ImageButtons will want to use resources.SquareButton as the background image.
    """
    def __init__(
                self, image, action, x, y, parent_group = None, 
                image_2=None, anchor='bottomleft'
            ):
        """
        @param image: Button background image
        @param action: Function to call when pressed
        @param x, y: Bottom left corner position
        @param parent_group: L{ButtonGroup} that owns this object
        @param image_2: Second image to draw over background.
        """
        super(ImageButton,self).__init__(
            image, action, x, y, "", parent_group, None
        )
        self.image_2 = image_2
        self.anchor = anchor

    def draw(self):
        color = (1,1,1,1)
        if self.parent_group != None and self.selected:
            color = (0.8, 0.8, 0.8, 1)
        if self.pressed: color = (0.7, 0.7, 0.7, 1)
        draw.set_color(color=color)
        draw.image(self.image,self.x,self.y)
        if self.image_2 != None:
            if self.anchor == 'bottomleft':
                draw.image(self.image_2, self.x, self.y)
            elif self.anchor == 'center':
                draw.image(
                    self.image_2, 
                    self.x+self.image.width/2, self.y+self.image.height/2
                )

class ButtonGroup(object):
    """
    Radio button behavior. Init with a list of buttons (optional) and add new buttons as necessary.
    """
    def __init__(self, buttons=None):
        """
        @param buttons: A list of buttons. Please do not be phased by the defaul value of None.
        """
        #Weird shit was going on here. Button groups were somehow inheriting 
        #the lists of previous other groups. This little idiom seems to have 
        #fixed that problem, though I'm not exactly sure why.
        if buttons == None: buttons = []
        self.buttons = buttons
        if len(self.buttons) > 0:
            self.buttons[0].selected = True
            for button in self.buttons:
                button.parent_group = self
    
    def add(self, button):
        self.buttons.append(button)
    
    def select(self, select_button):
        """Internal use only. Called by individual buttons when they are clicked."""
        if not select_button in self.buttons: return
        for button in self.buttons:
            if button == select_button:
                button.selected = True
            else:
                button.selected = False
