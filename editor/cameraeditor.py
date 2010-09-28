import glydget

import abstracteditor, editorstate
from engine import gamestate
from engine.util import draw

w = 1280
h = 720
hw = w//2
hh = h//2

class CameraEditor(abstracteditor.AbstractEditor):
    def __init__(self, ed):
        super(CameraEditor, self).__init__(ed)
        
        self.camera_pallet = glydget.Window("Camera Tools", [
            glydget.Button('New camera point', self.new_camera_point),
            glydget.Button('Delete camera point', self.delete_camera_point),
        ])
        self.camera_pallet.show()
        self.camera_pallet.move(gamestate.main_window.width - 2 - self.camera_pallet.width, 
                                gamestate.main_window.height - 162)
        gamestate.main_window.push_handlers(self.camera_pallet)
        
        self.cpoint_identifier_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.cpoint_x_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.cpoint_y_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.inspector = glydget.Window("Camera Point Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.cpoint_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.cpoint_x_field], True),
            glydget.HBox([glydget.Label('y'), self.cpoint_y_field], True),
        ])
        self.inspector.move(2, gamestate.main_window.height-2)
    
    def wants_drag(self, x, y):
        self.dragging_item = self.scene.camera.camera_point_near_point((x, y))
        return self.dragging_item is not None
    
    def start_drag(self, x, y):
        self.drag_start = (x, y)
        self.drag_anchor = self.dragging_item.position
    
    def continue_drag(self, x, y):
        self.is_dragging_item = True
        new_point = (self.drag_anchor[0] - (self.drag_start[0] - x),
                     self.drag_anchor[1] - (self.drag_start[1] - y))
        new_point = (min(max(new_point[0], hw), self.scene.env.width-hw),
                     min(max(new_point[1], hh), self.scene.env.height-hh))
        self.dragging_item.position = new_point
    
    def end_drag(self, x, y):
        self.is_dragging_item = False
        if self.dragging_item:
            self.set_selected_item(self.dragging_item)
        self.dragging_item = None
    
    def update_item_from_inspector(self, widget=None):
        if self.selected_item:
            new_id = self.cpoint_identifier_field.text
            if new_id != self.selected_item.identifier:
                self.scene.camera.remove_point(self.selected_item.identifier)
                new_point = self.scene.camera.add_point(int(self.cpoint_x_field.text), 
                                                        int(self.cpoint_y_field.text),
                                                        self.cpoint_identifier_field.text)
                self.selected_item = new_point
            else:
                self.selected_item.position = (int(self.cpoint_x_field.text), 
                                               int(self.cpoint_y_field.text))
    
    def update_inspector_from_item(self, widget=None):
        self.cpoint_identifier_field.text = self.selected_item.identifier
        self.cpoint_x_field.text = str(int(self.selected_item.position[0]))
        self.cpoint_y_field.text = str(int(self.selected_item.position[1]))
    
    
    def draw(self, dt=0):
        if self.camera_pallet.batch:
            self.camera_pallet.batch.draw()
        if self.inspector.batch:
            self.inspector.batch.draw()
        
        self.editor.scene.camera.apply()
        draw.set_color(1,0,1,1)
        for point in self.scene.camera.points.viewvalues():
            p = point.position
            draw.rect(p[0]-5, p[1]-5, p[0]+5, p[1]+5)
        p = self.dragging_item or self.selected_item
        if p:
            draw.rect_outline(p.position[0]-hw, p.position[1]-hh, 
                              p.position[0]+hw, p.position[1]+hh)
        self.editor.scene.camera.unapply()
    
    def new_camera_point(self, button=None):
        editorstate.set_status_message("Click to place a camera point")
        def point_placer(x, y):
            self.editor.change_selection(self)
            self.set_selected_item(self.scene.camera.add_point(x, y))
            editorstate.set_status_message('')
        self.editor.click_actions.append(point_placer)
    
    def delete_camera_point(self, button=None):
        def point_deleter(x, y):
            self.scene.camera.remove_point(self.scene.camera.camera_point_near_point((x, y)))
            editorstate.set_status_message('')
        self.editor.click_actions.append(point_deleter)
        editorstate.set_status_message("Click a camera point to delete it")
    
