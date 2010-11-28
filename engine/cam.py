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
    def __init__(self, actions, x, y, ui):
        self.visible = False
        self.actions = actions
        self.x = x
        self.y = y
        # JK LOL
        self.x, self.y = 0, 0
        self.hide_on_click_outside = True
        self.ui = ui
        
        self.background_sprite = pyglet.sprite.Sprite(
                                    pyglet.resource.image('ui/options_box_red.png'),
                                    x=0, y=0)
        self.batch = pyglet.graphics.Batch()
        self.buttons = []
        self.labels = set()
        
        rects = [(90, 138, 330, 40), (455, 130, 380, 40), (880, 138, 330, 40), 
                 (90, 70, 330, 40),  (455, 70, 380, 40), (880, 70, 330, 40)]
        print rects
        
        self.sound_for_callback = {}
        
        for i, (text, callback) in enumerate(self.actions.viewitems()):
            rect = rects[i]
            self.sound_for_callback[callback] = pyglet.resource.media('sound/select_%d.wav' % (i+1),
                                                                      streaming=False)
            self.buttons.append((rect, callback))
            self.labels.add(pyglet.text.Label("%d: %s" % (i+1, text), multiline=True,
                                    font_name=['Synchro LET', 'Verdana', 'Helvetica'],
                                    x=rect[0], y=rect[1], width=rect[2], height=rect[3],
                                    font_size=12, anchor_y="top",
                                    batch=self.batch, color=(255,255,255,255)))
        
        self.set_visible(True)
        
    
    # Make this into a property instead. I can't remember how right now. --Steve
    def set_visible(self, visible):
        if visible:
            gamestate.event_manager.set_cam(self)
        else:
            gamestate.event_manager.set_cam(None)
            self.ui.cam = None
            for l in self.labels:
                l.delete()
        self.visible = visible
    
    # Handle an event
    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            callback = self.button_under(x,y)
            if callback is None:
                if self.hide_on_click_outside:
                    self.set_visible(False)
                # pass this even down to other handlers, clean up the CAM
                return pyglet.event.EVENT_UNHANDLED
            else:
                # execute the click action and clean up the CAM
                self.sound_for_callback[callback].play()
                callback()
                self.set_visible(False)
                self.ui.clean_cam()
                return pyglet.event.EVENT_HANDLED
    
    def on_key_release(self, symbol, modifiers):
        nums = {getattr(pyglet.window.key,"_%d" % (i+1)): self.buttons[i][1] for i in range(len(self.buttons))}
        for num, callback in nums.viewitems():
            if num == symbol:
                self.sound_for_callback[callback].play()
                callback()
                self.set_visible(False)
                self.ui.clean_cam()
                return pyglet.event.EVENT_HANDLED
    
    # Determines which button is under the given point
    # Note that this function's behaviour is undefined when buttons overlap
    # this is intended but should later be changed to return the topmost button
    def button_under(self, x, y):
        print x, y
        for rect, callback in self.buttons:
            if rect[0] < x < rect[0]+rect[2] and rect[1]-rect[3] < y < rect[1]:
                return callback
        return None
    
    def draw(self, dt=0):
        if(self.visible):
            self.background_sprite.draw()
            self.batch.draw()
    
