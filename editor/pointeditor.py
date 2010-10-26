import glydget

import abstracteditor, editorstate
from engine import gamestate
from engine.util import draw

class PointEditor(abstracteditor.AbstractEditor):
    def __init__(self, ed):
        super(PointEditor, self).__init__(ed)
        
        self.point_identifier_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.point_x_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.point_y_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.inspector = glydget.Window("Point Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.point_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.point_x_field], True),
            glydget.HBox([glydget.Label('y'), self.point_y_field], True),
            glydget.Button('New edge out (o)', self.new_edge_from_point),
        ])
        self.inspector.move(2, gamestate.main_window.height-2)
        
        self.placing_point = False
    
    def wants_drag(self, x, y):
        if self.placing_point:
            self.editor.change_selection(self)
            self.set_selected_item(self.scene.walkpath.add_point(x, y))
            editorstate.set_status_message('')
            return True
        else:
            self.dragging_item = self.scene.walkpath.path_point_near_point((x, y))
            return self.dragging_item is not None
    
    def start_drag(self, x, y):
        if not self.placing_point:
            self.drag_start = (x, y)
            self.drag_anchor = self.scene.walkpath.points[self.dragging_item]
    
    def continue_drag(self, x, y):
        if not self.placing_point:
            new_point = (self.drag_anchor[0] - (self.drag_start[0] - x),
                         self.drag_anchor[1] - (self.drag_start[1] - y))
            self.is_dragging_item = True
            self.scene.walkpath.points[self.dragging_item] = new_point
            for actor in self.scene.actors.viewvalues():
                if actor.walkpath_point == self.dragging_item:
                    actor.sprite.position = new_point
    
    def end_drag(self, x, y):
        if not self.placing_point:
            self.is_dragging_item = False
            if self.dragging_item:
                self.set_selected_item(self.dragging_item)
            self.dragging_item = False
        self.placing_point = False
    
    def update_item_from_inspector(self, widget=None):
        if self.selected_item:
            old_identifier = self.selected_item
            new_identifier = self.point_identifier_field.text
            if old_identifier != new_identifier:
                self.selected_item = new_identifier
                for edge in self.scene.walkpath.edges.viewvalues():
                    if edge.a == old_identifier:
                        edge.a = new_identifier
                    if edge.b == old_identifier:
                        edge.b = new_identifier
                for actor in self.scene.actors.viewvalues():
                    if actor.walkpath_point == old_identifier:
                        actor.walkpath_point = new_identifier
            self.scene.walkpath.remove_point(old_identifier)
            self.scene.walkpath.add_point(int(self.point_x_field.text), 
                                          int(self.point_y_field.text), 
                                          new_identifier)
    
    def update_inspector_from_item(self, widget=None):
        self.point_identifier_field.text = self.selected_item
        self.point_x_field.text = str(int(self.scene.walkpath.points[self.selected_item][0]))
        self.point_y_field.text = str(int(self.scene.walkpath.points[self.selected_item][1]))
    
    def draw(self, dt=0):
        if self.inspector.batch:
            self.inspector.batch.draw()
        
        self.editor.scene.camera.apply()
        wp = self.scene.walkpath
        wp.draw()
        if self.selected_item:
            point = wp.points[self.selected_item]
            draw.set_color(1,1,0,1)
            draw.rect(point[0]-2, point[1]-2, point[0]+2, point[1]+2)
        self.editor.scene.camera.unapply()
    
    def new_point(self, button=None):
        editorstate.set_status_message("Click to place a point")
        self.placing_point = True
    
    def delete_point(self, button=None):
        def point_deleter(x, y):
            self.scene.walkpath.remove_point(self.scene.walkpath.path_point_near_point((x, y)))
            editorstate.set_status_message('')
        self.editor.click_actions.append(point_deleter)
        editorstate.set_status_message("Click a point to delete it")
    
    def new_edge_from_point(self, button=None):
        if not self.selected_item:
            return
        self.point_1 = self.selected_item
        def edge_finish(x, y):
            self.point_2 = self.scene.walkpath.path_point_near_point((x, y))
            if not self.point_2:
                self.point_2 = self.scene.walkpath.add_point((x, y))
            if self.point_1 != self.point_2:
                self.editor.change_selection(self.editor.edge_ed)
                new_edge = self.scene.walkpath.add_edge(self.point_1, self.point_2)
                self.editor.edge_ed.set_selected_item(new_edge)
            editorstate.set_status_message('')
        editorstate.set_status_message('Click to place the destination point')
        self.editor.click_actions.append(edge_finish)
    
