import glydget

import abstracteditor, editorstate
from engine import gamestate
from engine.util import draw, vector

class EdgeEditor(abstracteditor.AbstractEditor):
    def __init__(self, ed):
        super(EdgeEditor, self).__init__(ed)
        self.closest_edge = None
        self.point_1 = None
        self.point_2 = None
        
        self.edge_pallet = glydget.Window("Edge Tools", [
            glydget.Button('Select edge (e)', self.new_edge),
            glydget.Button('New point (p)', self.editor.point_ed.new_point),
            glydget.Button('New edge', self.new_edge),
            glydget.Button('Delete point', self.editor.point_ed.delete_point),
            glydget.Button('Delete edge', self.delete_edge),
        ])
        self.edge_pallet.show()
        self.edge_pallet.move(gamestate.main_window.width - 2 - self.edge_pallet.width, 
                              gamestate.main_window.height - 97)
        gamestate.main_window.push_handlers(self.edge_pallet)
        
        self.edge_a_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.edge_b_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.edge_anim_field = glydget.Entry('', on_change=self.update_item_from_inspector)
        self.inspector = glydget.Window("Edge Inspector", [
            glydget.HBox([glydget.Label('a'), self.edge_a_field], True),
            glydget.HBox([glydget.Label('b'), self.edge_b_field], True),
            glydget.Button('Subdivide (d)', self.subdivide_edge),
        ])
        self.inspector.move(2, gamestate.main_window.height-2)
    
    def wants_drag(self, x, y):
        return True
    
    def end_drag(self, x, y):
        world_point = self.scene.camera.mouse_to_canvas(x, y)
        self.set_selected_item(self.scene.walkpath.closest_edge_to_point(world_point))
    
    def draw(self, dt=0):
        if self.edge_pallet.batch:
            self.edge_pallet.batch.draw()
        if self.inspector.batch:
            self.inspector.batch.draw()
        
        if self.selected_item:
            p = self.editor.mouse
            cp = self.scene.walkpath.closest_edge_point_to_point(self.selected_item, p)
            draw.set_color(1,1,0,1)
            draw.rect(cp[0]-3, cp[1]-3, cp[0]+3, cp[1]+3)
    
    def update_item_from_inspector(self, widget=None):
        if self.selected_item:
            self.scene.walkpath.remove_edge(self.selected_item.a, self.selected_item.b)
            self.scene.walkpath.add_edge(self.edge_a_field.text, self.edge_b_field.text,
                                anim=self.edge_anim_field.text)
    
    def update_inspector_from_item(self, widget=None):
        self.edge_a_field.text = self.selected_item.a
        self.edge_b_field.text = self.selected_item.b
        self.edge_anim_field.text = self.selected_item.anim or ''
    
    def new_edge(self, button=None):
        editorstate.set_status_message('Click the source point')
        def edge_setup(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_1 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_1:
                editorstate.set_status_message('Click the destination point')
            else:
                # empty the queue, never mind
                self.editor.click_actions = collections.deque()
                editorstate.set_status_message('')
        def edge_finish(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_2 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_2 and self.point_1 != self.point_2:
                self.set_selected_item(self.scene.walkpath.add_edge(self.point_1, self.point_2))
            editorstate.set_status_message('')
        self.editor.click_actions.append(edge_setup)
        self.editor.click_actions.append(edge_finish)
    
    def delete_edge(self, button=None):
        editorstate.set_status_message('Click the source point')
        def edge_setup(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_1 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_1:
                editorstate.set_status_message('Click the destination point')
            else:
                # empty the queue, never mind
                self.click_actions = collections.deque()
                editorstate.set_status_message('')
        def edge_finish(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_2 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_2:
                self.set_selected_item(None)
                self.scene.walkpath.remove_edge(self.point_1, self.point_2)
            editorstate.set_status_message('')
        self.editor.click_actions.append(edge_setup)
        self.editor.click_actions.append(edge_finish)
    
    def subdivide_edge(self, button=None):
        if not self.selected_item:
            return
        p1 = self.scene.walkpath.points[self.selected_item.a]
        p2 = self.scene.walkpath.points[self.selected_item.b]
        p1name = self.selected_item.a
        p2name = self.selected_item.b
        midpoint_coords = self.scene.walkpath.closest_edge_point_to_point(self.selected_item, self.editor.mouse)
        if vector.length_squared(vector.tuple_op(p1, midpoint_coords)) < 10 \
        or vector.length_squared(vector.tuple_op(p2, midpoint_coords)) < 10:
            midpoint_coords = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        midpoint = self.scene.walkpath.add_point(*vector.round_down(midpoint_coords))
        self.selected_item.b = midpoint
        new_edge = self.scene.walkpath.add_edge(midpoint, p2name, anim=self.selected_item.anim)
        if self.selected_item.counterpart:
            self.selected_item.counterpart.a = midpoint
            new_cp = self.scene.walkpath.add_edge(p2name, midpoint, anim=self.selected_item.counterpart.anim)
    
