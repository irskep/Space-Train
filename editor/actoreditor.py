import glydget, os

import abstracteditor, editorstate
from engine import gamestate
from engine.util import draw, settings

class ActorEditor(abstracteditor.AbstractEditor):
    def __init__(self, ed):
        super(ActorEditor, self).__init__(ed)
        
        self.actor_pallet = glydget.Window("Make Actor", [
            glydget.Button(actor_name, self.actor_button_action) \
            for actor_name in os.listdir(os.path.join(settings.resources_path, 'actors'))
            if actor_name != '.DS_Store'
        ])
        self.actor_pallet.show()
        self.actor_pallet.move(gamestate.main_window.width - 2 - self.actor_pallet.width, 
                               gamestate.main_window.height - 242)
        gamestate.main_window.push_handlers(self.actor_pallet)
        
        self.id_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.state_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.scale_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.x_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.y_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.wp_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.inspector = glydget.Window("Actor Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.id_field], True),
            glydget.HBox([glydget.Label('Start state'), self.state_field], True),
            glydget.HBox([glydget.Label('Scale'), self.scale_field], True),
            glydget.HBox([glydget.Label('x'), self.x_field], True),
            glydget.HBox([glydget.Label('y'), self.y_field], True),
            glydget.HBox([glydget.Label('Walkpath point'), self.wp_field], True),
            glydget.Button('Delete', self.delete_selected_actor)
        ])
        self.inspector.move(2, gamestate.main_window.height-2)
    
    def wants_drag(self, x, y):
        self.dragging_item = self.scene.actor_under_point(x, y)
        return self.dragging_item is not None
    
    def start_drag(self, x, y):
        self.drag_start = (x, y)
        self.drag_anchor = self.dragging_item.sprite.position
    
    def continue_drag(self, x, y):
        new_point = (self.drag_anchor[0] - (self.drag_start[0] - x),
                     self.drag_anchor[1] - (self.drag_start[1] - y))
        if self.dragging_item.walkpath_point is None:
            self.is_dragging_item = True
            self.dragging_item.sprite.position = new_point
    
    def update_item_from_inspector(self, widget=None):
        if self.selected_item:
            del self.scene.actors[self.selected_item.identifier]
            self.selected_item.identifier = self.id_field.text
            self.scene.actors[self.selected_item.identifier] = self.selected_item
            
            self.selected_item.update_state(self.state_field.text)
            self.selected_item.sprite.scale = float(self.scale_field.text)
            
            wp = self.wp_field.text
            if wp and self.scene.walkpath.points.has_key(wp):
                self.selected_item.walkpath_point = wp
                self.selected_item.sprite.position = self.scene.walkpath.points[wp]
            else:
                self.wp_field.text = ''
                self.selected_item.walkpath_point = None
                self.selected_item.sprite.x = int(self.x_field.text)
                self.selected_item.sprite.y = int(self.y_field.text)
    
    def update_inspector_from_item(self, widget=None):
        self.id_field.text = self.selected_item.identifier
        self.state_field.text = self.selected_item.current_state
        wp = self.selected_item.walkpath_point
        if wp and self.scene.walkpath.points.has_key(wp):
            self.wp_field.text = wp
        else:
            self.wp_field.text = ''
            self.selected_item.walkpath_point = None
        self.x_field.text = str(int(self.selected_item.sprite.x))
        self.y_field.text = str(int(self.selected_item.sprite.y))
        self.scale_field.text = str(float(self.selected_item.sprite.scale))
    
    def draw(self, dt=0):
        if self.actor_pallet.batch:
            self.actor_pallet.batch.draw()
        if self.inspector.batch:
            self.inspector.batch.draw()
        
        if self.selected_item:
            self.editor.scene.camera.apply()
            s = self.selected_item.sprite
            img = self.selected_item.current_image()
            ax = img.anchor_x*self.selected_item.sprite.scale
            ay = img.anchor_y*self.selected_item.sprite.scale
            min_x = s.x - ax
            min_y = s.y - ay
            max_x = s.x - ax + img.width*self.selected_item.sprite.scale
            max_y = s.y - ay + img.height*self.selected_item.sprite.scale
            draw.set_color(1, 0, 0, 1)
            draw.rect_outline(min_x, min_y, max_x, max_y)
            self.editor.scene.camera.unapply()
    
    def actor_button_action(self, button=None):
        def actor_placer(x, y):
            self.dragging_item = self.scene.new_actor(button.text,
                                                      attrs = {'x': x, 'y': y})
            editorstate.set_status_message('')
        self.editor.click_actions.append(actor_placer)
        editorstate.set_status_message("Click to place %s" % button.text)
    
    def delete_selected_actor(self, button=None):
        actor_to_delete = self.selected_item
        self.set_selected_item(None)
        self.scene.remove_actor(actor_to_delete.identifier)
    
