import os, pyglet, glydget

from engine import scene, gamestate, settings, actor

import draw

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        gamestate.main_window.push_handlers(self)
        
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
        self.is_dragging_camera = False
        self.is_dragging_object = False
        self.dragging_object = None
        self.selected_actor = None
        self.actor_name = None
        
        self.status_label = pyglet.text.Label('', x=gamestate.main_window.width, 
                                              y=gamestate.main_window.height, 
                                              font_name = "Gill Sans",
                                              font_size = 12,
                                              color = (0,0,0,255),
                                              anchor_x='right', anchor_y='top')
        
        self.actor_pallet = glydget.Window("Actors", [
            glydget.Button(actor_name, self.actor_button_action) \
            for actor_name in os.listdir(os.path.join(settings.resources_path, 'actors'))
        ])
        self.actor_pallet.show()
        self.actor_pallet.move(gamestate.main_window.width-2 - self.actor_pallet.width, 
                               gamestate.main_window.height-2)
        gamestate.main_window.push_handlers(self.actor_pallet)
        
        self.actor_identifier_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_x_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_y_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_inspector = glydget.Window("Actor Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.actor_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.actor_x_field], True),
            glydget.HBox([glydget.Label('y'), self.actor_y_field], True),
        ])
        self.actor_inspector.move(2, gamestate.main_window.height-2)
        gamestate.move_camera(1)
    
    def set_selected_actor(self, new_actor):
        if new_actor is None and self.selected_actor is not None:
            self.update_actor_from_inspector()
            self.selected_actor = new_actor
            self.actor_inspector.hide()
            gamestate.main_window.pop_handlers()
        else:
            if new_actor is not None and self.selected_actor is None:
                self.actor_inspector.show()
                gamestate.main_window.push_handlers(self.actor_inspector)
            elif new_actor != self.selected_actor:
                self.update_actor_from_inspector()
            self.selected_actor = new_actor
            self.update_inspector_from_actor()
    
    def update_inspector_from_actor(self):
        self.actor_identifier_field.text = self.selected_actor.identifier
        self.actor_x_field.text = str(int(self.selected_actor.sprite.x))
        self.actor_y_field.text = str(int(self.selected_actor.sprite.y))
    
    def update_actor_from_inspector(self):
        if self.selected_actor:
            self.selected_actor.identifier = self.actor_identifier_field.text
            self.selected_actor.sprite.x = int(self.actor_x_field.text)
            self.selected_actor.sprite.y = int(self.actor_y_field.text)
    
    
    # Events
    def actor_button_action(self, button):
        self.actor_name = button.text
        self.status_label.begin_update()
        self.status_label.text = "Click to place %s" % self.actor_name
        self.status_label.end_update()
    
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
        if modifiers & (pyglet.window.key.MOD_ACCEL):
            if symbol == pyglet.window.key.S:
                self.scene.save_info()
                return True
    
    def on_mouse_press(self, x, y, button, modifiers):
        world_point = gamestate.mouse_to_canvas(x, y)
        if modifiers & (pyglet.window.key.MOD_ALT | pyglet.window.key.MOD_OPTION):
            self.drag_start = (x, y)
            self.drag_anchor = (gamestate.camera_x, gamestate.camera_y)
            self.is_dragging_camera = True
        elif self.actor_name is None:
            self.dragging_object = self.scene.actor_under_point(*world_point)
        elif self.actor_name:
            self.dragging_object = self.scene.new_actor(self.actor_name, x=world_point[0], y=world_point[1])
        
        if self.dragging_object:
            self.drag_start = (x, y)
            self.drag_anchor = self.dragging_object.sprite.position
            self.is_dragging_object = False
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.is_dragging_camera:
            gamestate.set_camera(self.drag_anchor[0] + self.drag_start[0] - x,
                                 self.drag_anchor[1] + self.drag_start[1] - y, update_target=True)
        elif self.dragging_object:
            self.is_dragging_object = True
            self.dragging_object.sprite.position = (self.drag_anchor[0] - (self.drag_start[0] - x),
                                                    self.drag_anchor[1] - (self.drag_start[1] - y))
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_dragging_camera:
            self.is_dragging_camera = False
            gamestate.camera_target_x = gamestate.camera_x
            gamestate.camera_target_y = gamestate.camera_y
        elif self.is_dragging_object:
            self.is_dragging_object = False
            self.scene.update_actor_info(self.dragging_object)
        if isinstance(self.dragging_object, actor.Actor) or self.dragging_object is None:
            self.set_selected_actor(self.dragging_object)
        if self.actor_name:
            self.actor_name = None
            self.scene.update_actor_info(self.dragging_object)
            self.status_label.begin_update()
            self.status_label.text = ''
            self.status_label.end_update()
        self.dragging_object = None
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        gamestate.set_camera(gamestate.camera_x - scroll_x*4, gamestate.camera_y + scroll_y*4, update_target=True)
    
    
    # Update/Draw
    def update(self, dt):
        self.check_camera_keys()
    
    def draw(self):
        self.scene.draw()
        self.actor_pallet.batch.draw()
        if self.actor_inspector.batch:
            self.actor_inspector.batch.draw()
        draw.set_color(1,1,1,1)
        l = self.status_label
        draw.rect(l.x-l.content_width, l.y-l.content_height, l.x, l.y)
        self.status_label.draw()
    

