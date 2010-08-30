import os, pyglet, glydget, collections

from engine import scene, actor
from engine import gamestate, settings, util

import draw

class EditorView(object):
    def __init__(self, scene_name):
        self.scene = scene.Scene(scene_name)
        gamestate.main_window.push_handlers(self)
        
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
        self.mouse = (0, 0)
        self.is_dragging_camera = False
        self.is_dragging_object = False
        self.is_dragging_point = False
        self.is_dragging_cpoint = False
        self.dragging_actor = None
        self.dragging_point = None
        self.dragging_cpoint = None
        self.selected_actor = None
        self.selected_point = None
        self.selected_cpoint = None
        self.selected_edge = None
        self.closest_edge = None
        self.point_1 = None
        self.point_2 = None
        
        self.click_actions = collections.deque()
        
        self.status_label = pyglet.text.Label('', x=gamestate.main_window.width, 
                                              y=gamestate.main_window.height, 
                                              font_name = "Courier New",
                                              font_size = 12,
                                              color = (0,0,0,255),
                                              anchor_x='right', anchor_y='top')
        
        self.init_gui()
        self.scene.camera.update(1)
    
    def init_gui(self):
        self.actor_pallet = glydget.Window("Make Actor", [
            glydget.Button(actor_name, self.actor_button_action) \
            for actor_name in os.listdir(os.path.join(settings.resources_path, 'actors'))
        ])
        self.actor_pallet.show()
        self.actor_pallet.move(gamestate.main_window.width - 2 - self.actor_pallet.width, 
                               gamestate.main_window.height - 22)
        gamestate.main_window.push_handlers(self.actor_pallet)
        
        self.edge_pallet = glydget.Window("Edge Tools", [
            glydget.Button('Select edge (e)', self.new_edge),
            glydget.Button('New point (p)', self.new_point),
            glydget.Button('New edge', self.new_edge),
            glydget.Button('Delete point', self.delete_point),
            glydget.Button('Delete edge', self.delete_edge),
        ])
        self.edge_pallet.show()
        self.edge_pallet.move(gamestate.main_window.width-2 - self.edge_pallet.width, 
                              self.actor_pallet.y - self.actor_pallet.height - 2)
        gamestate.main_window.push_handlers(self.edge_pallet)
        
        self.camera_pallet = glydget.Window("Camera Tools", [
            glydget.Button('New camera point', self.new_camera_point),
            glydget.Button('Delete camera point', self.delete_camera_point),
        ])
        self.camera_pallet.show()
        self.camera_pallet.move(gamestate.main_window.width-2 - self.camera_pallet.width, 
                                self.edge_pallet.y - self.edge_pallet.height - 2)
        gamestate.main_window.push_handlers(self.camera_pallet)
        
        self.actor_identifier_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_x_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_y_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_walkpoint_field = glydget.Entry('', on_change=self.update_actor_from_inspector)
        self.actor_inspector = glydget.Window("Actor Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.actor_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.actor_x_field], True),
            glydget.HBox([glydget.Label('y'), self.actor_y_field], True),
            glydget.HBox([glydget.Label('Walkpath point'), self.actor_walkpoint_field], True),
        ])
        self.actor_inspector.move(2, gamestate.main_window.height-2)
        
        self.point_identifier_field = glydget.Entry('', on_change=self.update_point_from_inspector)
        self.point_x_field = glydget.Entry('', on_change=self.update_point_from_inspector)
        self.point_y_field = glydget.Entry('', on_change=self.update_point_from_inspector)
        self.point_inspector = glydget.Window("Point Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.point_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.point_x_field], True),
            glydget.HBox([glydget.Label('y'), self.point_y_field], True),
            glydget.Button('New edge out (o)', self.new_edge_from_point),
        ])
        self.point_inspector.move(2, gamestate.main_window.height-2)
        
        self.edge_a_field = glydget.Entry('', on_change=self.update_edge_from_inspector)
        self.edge_b_field = glydget.Entry('', on_change=self.update_edge_from_inspector)
        self.edge_anim_field = glydget.Entry('', on_change=self.update_edge_from_inspector)
        self.edge_inspector = glydget.Window("Edge Inspector", [
            glydget.HBox([glydget.Label('a'), self.edge_a_field], True),
            glydget.HBox([glydget.Label('b'), self.edge_b_field], True),
            glydget.Button('Subdivide (d)', self.subdivide_edge),
        ])
        self.edge_inspector.move(2, gamestate.main_window.height-2)
        
        self.cpoint_identifier_field = glydget.Entry('', on_change=self.update_camera_point_from_inspector)
        self.cpoint_x_field = glydget.Entry('', on_change=self.update_camera_point_from_inspector)
        self.cpoint_y_field = glydget.Entry('', on_change=self.update_camera_point_from_inspector)
        self.cpoint_inspector = glydget.Window("Camera Point Inspector", [
            glydget.HBox([glydget.Label('Identifier'), self.cpoint_identifier_field], True),
            glydget.HBox([glydget.Label('x'), self.cpoint_x_field], True),
            glydget.HBox([glydget.Label('y'), self.cpoint_y_field], True),
        ])
        self.cpoint_inspector.move(2, gamestate.main_window.height-2)
        
        self.windows = [self.actor_pallet, self.edge_pallet, self.camera_pallet,
                        self.actor_inspector, self.point_inspector, self.edge_inspector,
                        self.cpoint_inspector]
    
    def set_status_message(self, message=''):
        self.status_label.begin_update()
        self.status_label.text = message
        self.status_label.end_update()
    
    
    # Selection update crud
    def _selection_change_logic(self, attr_name, new_obj, inspector, obj_update, inspect_update):
        # All the complex logic here is just to deal with the fact that sometimes
        # the new or old value will be None, so sometimes the associated inspector
        # will be hidden and therefore its fields will be inaccessible.
        old_obj = getattr(self, attr_name)
        if old_obj is not None and new_obj is None:
            obj_update()
            setattr(self, attr_name, new_obj)
            inspector.hide()
            gamestate.main_window.pop_handlers()
        else:
            if old_obj is None and new_obj is not None:
                inspector.show()
                setattr(self, attr_name, new_obj)
                inspect_update()
                gamestate.main_window.push_handlers(inspector)
            elif new_obj != old_obj:
                obj_update()
            if old_obj:    
                setattr(self, attr_name, new_obj)
                inspect_update()
    
    def set_selected_actor(self, new_actor, recurse=True):
        if recurse and new_actor is not None:
            self.set_selected_point(None, False)
            self.set_selected_edge(None, False)
            self.set_selected_cpoint(None, False)
        self._selection_change_logic('selected_actor', new_actor, 
                                     self.actor_inspector, 
                                     self.update_actor_from_inspector,
                                     self.update_inspector_from_actor)
    
    def set_selected_point(self, new_point, recurse=True):
        if recurse and new_point is not None:
            self.set_selected_actor(None, False)
            self.set_selected_edge(None, False)
            self.set_selected_cpoint(None, False)
        self._selection_change_logic('selected_point', new_point, 
                                     self.point_inspector, 
                                     self.update_point_from_inspector,
                                     self.update_inspector_from_point)
    
    def set_selected_edge(self, new_edge, recurse=True):
        if recurse and new_edge is not None:
            self.set_selected_point(None, False)
            self.set_selected_actor(None, False)
            self.set_selected_cpoint(None, False)
        self._selection_change_logic('selected_edge', new_edge, 
                                     self.edge_inspector, 
                                     self.update_edge_from_inspector,
                                     self.update_inspector_from_edge)
    
    def set_selected_cpoint(self, new_point, recurse=True):
        if recurse and new_point is not None:
            self.set_selected_actor(None, False)
            self.set_selected_point(None, False)
            self.set_selected_edge(None, False)
        self._selection_change_logic('selected_cpoint', new_point, 
                                     self.cpoint_inspector, 
                                     self.update_camera_point_from_inspector,
                                     self.update_inspector_from_camera_point)
    
    def update_inspector_from_edge(self, widget=None):
        self.edge_a_field.text = self.selected_edge.a
        self.edge_b_field.text = self.selected_edge.b
        self.edge_anim_field.text = self.selected_edge.anim or ''
    
    def update_edge_from_inspector(self, widget=None):
        if self.selected_edge:
            self.scene.walkpath.remove_edge(self.selected_edge.a, self.selected_edge.b)
            self.scene.walkpath.add_edge(self.edge_a_field.text, self.edge_b_field.text,
                                anim=self.edge_anim_field.text)
    
    def update_inspector_from_point(self, widget=None):
        self.point_identifier_field.text = self.selected_point
        self.point_x_field.text = str(int(self.scene.walkpath.points[self.selected_point][0]))
        self.point_y_field.text = str(int(self.scene.walkpath.points[self.selected_point][1]))
    
    def update_point_from_inspector(self, widget=None):
        if self.selected_point:
            old_identifier = self.selected_point
            new_identifier = self.point_identifier_field.text
            if old_identifier != new_identifier:
                for edge in self.scene.walkpath.edges.viewvalues():
                    if edge.a == old_identifier:
                        edge.a = new_identifier
                    if edge.b == old_identifier:
                        edge.b = new_identifier
            self.scene.walkpath.remove_point(self.selected_point)
            self.scene.walkpath.add_point(int(self.point_x_field.text), int(self.point_y_field.text), 
                                          self.point_identifier_field.text)
    
    def update_inspector_from_camera_point(self, widget=None):
        self.cpoint_identifier_field.text = self.selected_cpoint.identifier
        self.cpoint_x_field.text = str(int(self.selected_cpoint.position[0]))
        self.cpoint_y_field.text = str(int(self.selected_cpoint.position[1]))
    
    def update_camera_point_from_inspector(self, widget=None):
        if self.selected_cpoint:
            self.scene.camera.remove_point(self.selected_cpoint.identifier)
            self.selected_cpoint = self.scene.camera.add_point(
                                        self.point_identifier_field.text, 
                                        int(self.cpoint_x_field.text), int(self.cpoint_y_field.text))
    
    def update_inspector_from_actor(self, widget=None):
        self.actor_identifier_field.text = self.selected_actor.identifier
        wp = self.selected_actor.walkpath_point
        if wp and self.scene.walkpath.points.has_key(wp):
            self.actor_walkpoint_field.text = wp
        else:
            self.actor_walkpoint_field.text = ''
            self.selected_actor.walkpath_point = None
        self.actor_x_field.text = str(int(self.selected_actor.sprite.x))
        self.actor_y_field.text = str(int(self.selected_actor.sprite.y))
    
    def update_actor_from_inspector(self, widget=None):
        if self.selected_actor:
            del self.scene.actors[self.selected_actor.identifier]
            self.selected_actor.identifier = self.actor_identifier_field.text
            self.scene.actors[self.selected_actor.identifier] = self.selected_actor
            
            wp = self.actor_walkpoint_field.text
            if wp and self.scene.walkpath.points.has_key(wp):
                self.selected_actor.walkpath_point = wp
                self.selected_actor.sprite.position = self.scene.walkpath.points[wp]
            else:
                self.actor_walkpoint_field.text = ''
                self.selected_actor.walkpath_point = None
                self.selected_actor.sprite.x = int(self.actor_x_field.text)
                self.selected_actor.sprite.y = int(self.actor_y_field.text)
    
    
    # Buttons
    def new_point(self, button=None):
        self.set_status_message("Click to place a point")
        def point_placer(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.set_selected_point(self.scene.walkpath.add_point(*world_point))
            self.set_status_message('')
        self.click_actions.append(point_placer)
    
    def delete_point(self, button=None):
        def point_deleter(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.scene.walkpath.remove_point(self.scene.walkpath.path_point_near_point(world_point))
            self.set_status_message('')
        self.click_actions.append(point_deleter)
        self.set_status_message("Click a point to delete it")
    
    def new_edge_from_point(self, button=None):
        if not self.selected_point:
            return
        self.point_1 = self.selected_point
        def edge_finish(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_2 = self.scene.walkpath.path_point_near_point(world_point)
            if not self.point_2:
                self.point_2 = self.scene.walkpath.add_point(*world_point)
            if self.point_1 != self.point_2:
                self.set_selected_edge(self.scene.walkpath.add_edge(self.point_1, self.point_2))
            self.set_status_message('')
        self.set_status_message('Click to place the destination point')
        self.click_actions.append(edge_finish)
    
    def new_camera_point(self, button=None):
        self.set_status_message("Click to place a camera point")
        def point_placer(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.set_selected_cpoint(self.scene.camera.add_point(*world_point))
            self.set_status_message('')
        self.click_actions.append(point_placer)
    
    def delete_camera_point(self, button=None):
        def point_deleter(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.scene.camera.remove_point(self.scene.camera.camera_point_near_point(world_point))
            self.set_status_message('')
        self.click_actions.append(point_deleter)
        self.set_status_message("Click a camera point to delete it")
    
    def new_edge(self, button=None):
        self.set_status_message('Click the source point')
        def edge_setup(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_1 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_1:
                self.set_status_message('Click the destination point')
            else:
                # empty the queue, never mind
                self.click_actions = collections.deque()
                self.set_status_message('')
        def edge_finish(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_2 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_2 and self.point_1 != self.point_2:
                self.set_selected_edge(self.scene.walkpath.add_edge(self.point_1, self.point_2))
            self.set_status_message('')
        self.click_actions.append(edge_setup)
        self.click_actions.append(edge_finish)
    
    def delete_edge(self, button=None):
        self.set_status_message('Click the source point')
        def edge_setup(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_1 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_1:
                self.set_status_message('Click the destination point')
            else:
                # empty the queue, never mind
                self.click_actions = collections.deque()
                self.set_status_message('')
        def edge_finish(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.point_2 = self.scene.walkpath.path_point_near_point(world_point)
            if self.point_2:
                self.set_selected_edge(None)
                self.scene.walkpath.remove_edge(self.point_1, self.point_2)
            self.set_status_message('')
        self.click_actions.append(edge_setup)
        self.click_actions.append(edge_finish)
    
    def subdivide_edge(self, button=None):
        if not self.selected_edge:
            return
        p1 = self.scene.walkpath.points[self.selected_edge.a]
        p2 = self.scene.walkpath.points[self.selected_edge.b]
        p1name = self.selected_edge.a
        p2name = self.selected_edge.b
        midpoint_coords = self.scene.walkpath.closest_edge_point_to_point(self.selected_edge, self.mouse)
        if util.dist_squared(util.tuple_op(p1, midpoint_coords)) < 10 \
        or util.dist_squared(util.tuple_op(p2, midpoint_coords)) < 10:
            midpoint_coords = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        midpoint = self.scene.walkpath.add_point(*util.round_down(midpoint_coords))
        self.selected_edge.b = midpoint
        new_edge = self.scene.walkpath.add_edge(midpoint, p2name, anim=self.selected_edge.anim)
        if self.selected_edge.counterpart:
            self.selected_edge.counterpart.a = midpoint
            new_cp = self.scene.walkpath.add_edge(p2name, midpoint, anim=self.selected_edge.counterpart.anim)
    
    def actor_button_action(self, button):
        def actor_placer(x, y):
            world_point = self.scene.camera.mouse_to_canvas(x, y)
            self.dragging_actor = self.scene.new_actor(button.text, x=world_point[0], y=world_point[1])
            self.set_status_message('')
        self.click_actions.append(actor_placer)
        self.set_status_message("Click to place %s" % button.text)
    
    
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
        else:
            actions = {
                pyglet.window.key.E: self.new_edge,
                pyglet.window.key.P: self.new_point,
                pyglet.window.key.D: self.subdivide_edge,
                pyglet.window.key.O: self.new_edge_from_point,
            }
            if actions.has_key(symbol):
                actions[symbol]()
    
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
            self.dragging_point = self.scene.walkpath.path_point_near_point(world_point)
            if self.dragging_point is None:
                self.dragging_cpoint = self.scene.camera.camera_point_near_point(world_point)
                if self.dragging_cpoint is None:
                    self.dragging_actor = self.scene.actor_under_point(*world_point)
        
        if self.dragging_actor:
            self.drag_start = (x, y)
            self.drag_anchor = self.dragging_actor.sprite.position
        elif self.dragging_point:
            self.drag_start = (x, y)
            self.drag_anchor = self.scene.walkpath.points[self.dragging_point]
        elif self.dragging_cpoint:
            self.drag_start = (x, y)
            self.drag_anchor = self.dragging_cpoint.position
    
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        new_point = (self.drag_anchor[0] - (self.drag_start[0] - x),
                     self.drag_anchor[1] - (self.drag_start[1] - y))
        if self.is_dragging_camera:
            self.scene.camera.set_position(self.drag_anchor[0] + (self.drag_start[0] - x),
                                           self.drag_anchor[1] + (self.drag_start[1] - y))
        elif self.dragging_actor and self.dragging_actor.walkpath_point is None:
            self.is_dragging_object = True
            self.dragging_actor.sprite.position = new_point
        elif self.dragging_point:
            self.is_dragging_point = True
            self.scene.walkpath.points[self.dragging_point] = new_point
            for actor in self.scene.actors.viewvalues():
                if actor.walkpath_point == self.dragging_point:
                    actor.sprite.position = new_point
        elif self.dragging_cpoint:
            self.is_dragging_cpoint = True
            new_point = (min(max(new_point[0], 512), self.scene.env.width-512),
                         min(max(new_point[1], 384), self.scene.env.height-384))
            self.dragging_cpoint.position = new_point
    
    def on_mouse_release(self, x, y, button, modifiers):
        # hacky hack because glydget doesn't handle mouse events properly >:-(
        for w in self.windows:
            if w._hit(x, y):
                return True
        
        self.is_dragging_camera = False
        self.is_dragging_object = False
        self.is_dragging_point = False
        self.set_selected_actor(self.dragging_actor)
        if self.dragging_point:
            self.set_selected_point(self.dragging_point)
        if self.dragging_cpoint:
            self.set_selected_cpoint(self.dragging_cpoint)
        if self.dragging_point is None and self.dragging_cpoint is None and self.dragging_actor is None:
            self.mouse = self.scene.camera.mouse_to_canvas(x, y)
            closest_point = None
            closest_dist = None
            wp = self.scene.walkpath
            for edge in wp.edges.viewvalues():
                cp = self.scene.walkpath.closest_edge_point_to_point(edge, self.mouse)
                test_dist = util.dist_squared((self.mouse[0]-cp[0], self.mouse[1]-cp[1]))
                if closest_dist is None or test_dist < closest_dist:
                    closest_point = cp
                    self.closest_edge = edge
                    closest_dist = test_dist
            self.set_selected_edge(self.closest_edge)
        self.dragging_cpoint = None
        self.dragging_point = None
        self.dragging_actor = None
    
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
        
        self.scene.camera.apply()
        self.draw_walkpath()
        self.draw_camera_points()
        
        if self.selected_actor:
            s = self.selected_actor.sprite
            min_x = s.x - s.image.anchor_x
            min_y = s.y - s.image.anchor_y
            max_x = s.x - s.image.anchor_x + s.image.width
            max_y = s.y - s.image.anchor_y + s.image.height
            draw.set_color(1, 0, 0, 1)
            draw.rect_outline(min_x, min_y, max_x, max_y)
        self.scene.camera.unapply()
        
        for w in self.windows:
            if w.batch:
                w.batch.draw()
        
        l = self.status_label
        if l.text:
            draw.set_color(1,1,1,1)
            draw.rect(l.x-l.content_width, l.y-l.content_height, l.x, l.y)
            self.status_label.draw()
    
    def draw_walkpath(self):    
        wp = self.scene.walkpath
        for edge in wp.edges.viewvalues():
            ax, ay = wp.points[edge.a]
            bx, by = wp.points[edge.b]
            if edge.counterpart:
                draw.line(ax, ay, bx, by, colors=(0, 255, 0, 255, 0, 255, 0, 255))
            else:
                draw.line(ax, ay, bx, by, colors=(255, 0, 0, 255, 0, 0, 255, 255))
        draw.set_color(1,0,0,1)
        for point in wp.points.viewvalues():
            draw.rect(point[0]-5, point[1]-5, point[0]+5, point[1]+5)
        if self.selected_point:
            point = wp.points[self.selected_point]
            draw.set_color(1,1,0,1)
            draw.rect(point[0]-2, point[1]-2, point[0]+2, point[1]+2)
        if self.selected_edge:
            cp = self.scene.walkpath.closest_edge_point_to_point(self.selected_edge, self.mouse)
            draw.set_color(1,1,0,1)
            draw.rect(cp[0]-3, cp[1]-3, cp[0]+3, cp[1]+3)
    
    def draw_camera_points(self):
        draw.set_color(1,0,1,1)
        for point in self.scene.camera.points.viewvalues():
            p = point.position
            draw.rect(p[0]-5, p[1]-5, p[0]+5, p[1]+5)
        p = self.dragging_cpoint or self.selected_cpoint
        if p:
            draw.rect_outline(p.position[0]-512, p.position[1]-384, p.position[0]+512, p.position[1]+384)
    

