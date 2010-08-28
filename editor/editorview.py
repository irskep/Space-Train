import os, pyglet, glydget

from engine import scene, gamestate, settings, actor

import sidebar

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        gamestate.main_window.push_handlers(self)
        
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
        self.is_dragging_camera = False
        self.is_dragging_object = False
        self.selected_object = None
        
        self.actor_name = None
        
        self.actor_window = glydget.Window ("Actors", [
            glydget.Button(actor_name, self.actor_button_action) \
            for actor_name in os.listdir(os.path.join(settings.resources_path, 'actors'))
        ])
        self.actor_window.show()
        self.actor_window.move(2, gamestate.norm_h-2)
        gamestate.main_window.push_handlers(self.actor_window)
        gamestate.move_camera(1)
    
    def actor_button_action(self, button):
        self.actor_name = button.text
    
    def check_camera_keys(self):
        if gamestate.keys[pyglet.window.key.LEFT]:
            gamestate.set_camera_target(gamestate.camera_target_x-10, gamestate.camera_target_y)
        if gamestate.keys[pyglet.window.key.RIGHT]:
            gamestate.set_camera_target(gamestate.camera_target_x+10, gamestate.camera_target_y)
        if gamestate.keys[pyglet.window.key.DOWN]:
            gamestate.set_camera_target(gamestate.camera_target_x, gamestate.camera_target_y-10)
        if gamestate.keys[pyglet.window.key.UP]:
            gamestate.set_camera_target(gamestate.camera_target_x, gamestate.camera_target_y+10)
    
    def on_key_press(self, symbol, modifiers):
        if modifiers & (pyglet.window.key.MOD_CTRL | pyglet.window.key.MOD_COMMAND):
            if symbol == pyglet.window.key.S:
                self.scene.save_info()
    
    def on_mouse_press(self, x, y, button, modifiers):
        if modifiers & (pyglet.window.key.MOD_ALT | pyglet.window.key.MOD_OPTION):
            self.drag_start = (x, y)
            self.drag_anchor = (gamestate.camera_x, gamestate.camera_y)
            self.is_dragging_camera = True
        else:
            world_point = gamestate.mouse_to_canvas(x, y)
            self.selected_object = self.scene.actor_under_point(*world_point)
            if self.selected_object:
                self.drag_start = (x, y)
                self.drag_anchor = self.selected_object.sprite.position
                self.is_dragging_object = False
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.is_dragging_camera:
            gamestate.set_camera(self.drag_anchor[0] + self.drag_start[0] - x,
                                 self.drag_anchor[1] + self.drag_start[1] - y, update_target=True)
        elif self.selected_object:
            self.is_dragging_object = True
            self.selected_object.sprite.position = (self.drag_anchor[0] - (self.drag_start[0] - x),
                                                    self.drag_anchor[1] - (self.drag_start[1] - y))
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_dragging_camera:
            self.is_dragging_camera = False
            gamestate.camera_target_x = gamestate.camera_x
            gamestate.camera_target_y = gamestate.camera_y
        elif self.is_dragging_object:
            self.is_dragging_object = False
            self.scene.info['actors'][self.selected_object.identifier]['x'] = self.selected_object.sprite.x
            self.scene.info['actors'][self.selected_object.identifier]['y'] = self.selected_object.sprite.y
            self.selected_object = None
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        gamestate.set_camera(gamestate.camera_x - scroll_x*4, gamestate.camera_y + scroll_y*4, update_target=True)
    
    def update(self, dt):
        self.check_camera_keys()
        # gamestate.move_camera(dt)
    
    def draw(self):
        self.scene.draw()
        self.actor_window.batch.draw()
    

