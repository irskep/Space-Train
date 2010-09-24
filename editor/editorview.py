import os, pyglet, glydget, collections

from engine import scene, actor
from engine import gamestate, settings
from engine.util import draw, vector

import pointeditor, actoreditor, cameraeditor, edgeeditor, pointeditor
import editorstate

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        gamestate.main_window.push_handlers(self)
        
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
        self.mouse = (0, 0)
        self.is_dragging_camera = False
        
        self.click_actions = collections.deque()
        
        self.cam_ed = cameraeditor.CameraEditor(self)
        self.point_ed = pointeditor.PointEditor(self)
        self.actor_ed = actoreditor.ActorEditor(self)
        self.edge_ed = edgeeditor.EdgeEditor(self)
        
        self.ed_with_selection = None
        self.ed_with_drag = None
        
        self.editors = [self.cam_ed, self.point_ed, self.actor_ed, self.edge_ed]
        self.windows = [self.actor_ed.actor_pallet, 
                        self.actor_ed.inspector, 
                        self.edge_ed.edge_pallet, 
                        self.edge_ed.inspector,
                        self.point_ed.inspector,
                        self.cam_ed.camera_pallet,
                        self.cam_ed.inspector]
        
        editorstate.init()
        
        self.scene.camera.update(1)
    
    def empty_click_actions(self):
        self.click_actions = collections.deque()
    
    def change_selection(self, new_ed_with_selection):
        if self.ed_with_selection is not None and self.ed_with_selection != new_ed_with_selection:
            self.ed_with_selection.set_selected_item(None)
        self.ed_with_selection = new_ed_with_selection
    
    
    # Other events
    def check_camera_keys(self):
        c = self.scene.camera
        if gamestate.keys[pyglet.window.key.LEFT]:
            c.set_target(c.target[0]-10, c.target[1])
        if gamestate.keys[pyglet.window.key.RIGHT]:
            c.set_target(c.target[0]+10, c.target[1])
        if gamestate.keys[pyglet.window.key.DOWN]:
            c.set_target(c.target[0], c.target[1]-10)
        if gamestate.keys[pyglet.window.key.UP]:
            c.set_target(c.target[0], c.target[1]+10)
    
    def on_key_press(self, symbol, modifiers):
        if modifiers & (pyglet.window.key.MOD_ACCEL):
            if symbol == pyglet.window.key.S:
                self.scene.save_info()
                return True
    
    def on_mouse_press(self, x, y, button, modifiers):
        # hacky hack
        for w in self.windows:
            if w._hit(x, y):
                return True
        
        if modifiers & (pyglet.window.key.MOD_ALT | pyglet.window.key.MOD_OPTION):
            self.drag_start = (x, y)
            self.drag_anchor = self.scene.camera.position
            self.is_dragging_camera = True
        elif len(self.click_actions) > 0:
            self.click_actions.popleft()(x, y)
        else:
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            for ed in self.editors:
                if ed.wants_drag(*world_point):
                    self.ed_with_drag = ed
                    break
            if self.ed_with_drag:
                self.ed_with_drag.start_drag(*world_point)
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        new_point = (self.drag_anchor[0] - (self.drag_start[0] - x),
                     self.drag_anchor[1] - (self.drag_start[1] - y))
        if self.is_dragging_camera:
            self.scene.camera.set_position(self.drag_anchor[0] + (self.drag_start[0] - x),
                                           self.drag_anchor[1] + (self.drag_start[1] - y))
        elif self.ed_with_drag is not None:
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.ed_with_drag.continue_drag(*world_point)
    
    def on_mouse_release(self, x, y, button, modifiers):
        # hacky hack because glydget doesn't handle mouse events properly >:-(
        for w in self.windows:
            if w._hit(x, y):
                return True
        
        self.is_dragging_camera = False
        if self.ed_with_drag:
            if self.ed_with_selection is not None and self.ed_with_drag != self.ed_with_selection:
                self.ed_with_selection.set_selected_item(None)
                self.ed_with_selection = None
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.ed_with_drag.end_drag(*world_point)
            if self.ed_with_drag.selected_item is not None:
                self.ed_with_selection = self.ed_with_drag
                self.ed_with_drag = None
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        c = self.scene.camera
        c.set_position(c.position[0] - scroll_x*4, c.position[1] + scroll_y*4)
        self.drag_start = (self.drag_start[0] - scroll_x*4, self.drag_start[1] - scroll_y*4)
    
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse = self.scene.camera.mouse_to_canvas(x, y)
    
    
    # Update/Draw
    def update(self, dt):
        self.check_camera_keys()
    
    def draw(self):
        self.scene.draw()
        
        for ed in self.editors:
            ed.draw()
        
        editorstate.draw()
    

