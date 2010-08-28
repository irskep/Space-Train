import pyglet

from engine import scene, gamestate

import sidebar

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        self.sidebar = sidebar.Sidebar()
        gamestate.sidebar_w = self.sidebar.width
        gamestate.main_window.push_handlers(self)
        self.sidebar.push_handlers()
        
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
        self.is_dragging = False
    
    def check_camera_keys(self):
        if gamestate.keys[pyglet.window.key.LEFT]:
            gamestate.set_camera_target(gamestate.camera_target_x-10, gamestate.camera_target_y)
        if gamestate.keys[pyglet.window.key.RIGHT]:
            gamestate.set_camera_target(gamestate.camera_target_x+10, gamestate.camera_target_y)
        if gamestate.keys[pyglet.window.key.DOWN]:
            gamestate.set_camera_target(gamestate.camera_target_x, gamestate.camera_target_y-10)
        if gamestate.keys[pyglet.window.key.UP]:
            gamestate.set_camera_target(gamestate.camera_target_x, gamestate.camera_target_y+10)
    
    def on_mouse_press(self, x, y, button, modifiers):
        if modifiers & (pyglet.window.key.MOD_ALT | pyglet.window.key.MOD_OPTION):
            self.drag_start = (x, y)
            self.drag_anchor = (gamestate.camera_x, gamestate.camera_y)
            self.is_dragging = True
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.is_dragging:
            gamestate.set_camera(self.drag_anchor[0] + self.drag_start[0] - x,
                                 self.drag_anchor[1] + self.drag_start[1] - y)
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.is_dragging = False
        gamestate.camera_target_x = gamestate.camera_x
        gamestate.camera_target_y = gamestate.camera_y
    
    def update(self, dt):
        self.check_camera_keys()
        if not self.is_dragging:
            gamestate.move_camera(dt)
    
    def draw(self):
        self.scene.draw()
        self.sidebar.draw()
    

