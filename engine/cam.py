"""
File:           cam.py
Author:         Fred Hatfull
Description:    A class encompassing the primary functionality of the Contextual Action Menu (CAM) in SPACE TRAIN.
Notes: 

Contextual Action Menu Life Cycle:
* A CAM instance is requested by a caller (scene, object, level script, something)
    * The caller must provide:
        + A reference to the UI object in use (will probably be a singleton/global)
        + A dictionary of available actions: {'action_name': [function or closure]}
        + A coordinate indicating the centre of menu area around which actions will appear
* A CAM is instantiated and attached to the UI object
    * When a CAM is instantiated it will not have to load any resources like sprites - these should be allocated as static resources somehow and associated with the CAM when it is created
* The CAM is set to visible to indicate that it should drawn by the UI each frame at the specified coordinates
* The CAM remains visible until it detects a click:
    * If the click is within a region controlled by the CAM (i.e. on an action button), the CAM calls the callback associated with the action
    * If the click is elsewhere, pass the event down the event stack and set the CAM to false.
        * Destroy the CAM instance?
"""

import copy, math
import json, pyglet
import gamestate, ui, util
from pyglet.window import key

class CAM(object):
    
    # Init
    def __init__(self, actions, x, y):
        print "Drawing CAM at (%d, %d)" % (x, y)
        self.visible = False
        self.actions = actions
        self.x = x
        self.y = y
        self.hide_on_click_outside = True

        self.batch = pyglet.graphics.Batch()
        self.buttons = []
        
        # Static resources, such as sprites for the CAM backgrounds
        sprites = {}
        sprite_batch = pyglet.graphics.Batch()
        sprites = {i: util.load_sprite(['ui', 'new_cam_%d.png' % i], batch = self.batch)
                    for i in xrange(1,7)}
        for s in sprites.viewvalues():
            s.anchor_x = s.width

        positioning = {}
        # positioning[1] = (150,187)
        # positioning[2] = (140,155)
        # positioning[3] = (130,120)
        # positioning[4] = (130,84)
        # positioning[5] = (140,48)
        # positioning[6] = (150,17)
        positioning[1] = (280,187)
        positioning[2] = (265,155)
        positioning[3] = (260,120)
        positioning[4] = (260,84)
        positioning[5] = (265,48)
        positioning[6] = (280,17)
        
        y -= sprites[1].height/2
                
        #defines the generic order in which CAM backrounds are used
        generic_item_order = [3, 4, 2, 5, 1, 6]
        
        used_items = []
        for action, callback in self.actions.items():
            used_items.append(generic_item_order.pop(0))
            
        used_items.sort()
                
        # Turn each action entry into a menu item
        for action, callback in self.actions.items():  
            count = used_items.pop(0)
            button = self.Button(x-sprites[1].width/3, y, 
                                 positioning[count][0], positioning[count][1],
                                 sprites[count], action, callback)
            self.buttons.append(button)
        
        self.set_visible(True)
        
    
    # Make this into a property instead. I can't remember how right now. --Steve
    def set_visible(self, visible):
        if visible:
            gamestate.event_manager.set_cam(self)
        else:
            gamestate.event_manager.set_cam(None)
        self.visible = visible
    
    # Handle an event
    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            button = self.button_under(x,y)
            if button is None:
                if self.hide_on_click_outside:
                    self.set_visible(False)
                # pass this even down to other handlers, clean up the CAM
                return pyglet.event.EVENT_UNHANDLED
            else:
                # execute the click action and clean up the CAM
                button.click()
                self.set_visible(False)
                return pyglet.event.EVENT_HANDLED
    
    def on_key_press(self, symbol, modifiers):
        button = 0
        if symbol == key.LEFT:
            self.buttons[button].set_x(self.buttons[button].x - 1)
        elif symbol == key.RIGHT:
            self.buttons[button].set_x(self.buttons[button].x + 1)
        elif symbol == key.UP:
            self.buttons[button].set_y(self.buttons[button].y + 1)
        elif symbol == key.DOWN:
            self.buttons[button].set_y(self.buttons[button].y - 1)
            
        print "Button %d: (%d, %d)" % (button, self.buttons[button].x, self.buttons[button].y)
    
    # Determines which button is under the given point
    # Note that this function's behaviour is undefined when buttons overlap
    # this is intended but should later be changed to return the topmost button
    def button_under(self, x, y):
        for button in self.buttons:
            if button.x <= x <= button.x + button.sprite.width \
            and button.y <= y <= button.y + button.sprite.height \
            and util.image_alpha_at_point(button.sprite.image, x-button.x, y-button.y) > 0:
                print 'alpha:', util.image_alpha_at_point(button.sprite.image, x-button.x, y-button.y)
                return button
        return None
    
    def draw(self, dt=0):
        if(self.visible):
            self.batch.draw()
            
    # TODO: finish button class
    class Button(object):
        def __init__(self, x, y, text_x, text_y, sprite, action, callback):
            self.sprite = sprite
            self.sprite.x = x
            self.sprite.y = y
            self.label = pyglet.text.Label(action, font_name = 'Times New Roman', 
                                           font_size = 14, anchor_x = 'right', 
                                           anchor_y = 'center', batch = self.sprite.batch, 
                                           color = (0, 0, 0, 255),
                                           x = self.sprite.x + text_x, 
                                           y = self.sprite.y + text_y)
            
            self.x = x
            self.y = y
            self.width = self.sprite.width
            self.height = self.sprite.height
            self.callback = callback
            
        def click(self):
            if(self.callback is not None):
				self.callback()
    
        def set_x(self, x):
            self.sprite.x = x
            self.label.x = self.sprite.x + ((self.sprite.width - 10) / 2)
            self.x = x
            
        def set_y(self, y):
            self.sprite.y = y
            self.label.y = (self.sprite.y + self.sprite.height) - (self.sprite.height / 2) - 5
            self.y = y
