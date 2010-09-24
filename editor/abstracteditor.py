from engine import gamestate

class AbstractEditor(object):
    def __init__(self, ed):
        super(AbstractEditor, self).__init__()
        self.editor = ed
        self.scene = self.editor.scene
        self.selected_item = None
        self.is_dragging_item = False
        self.dragging_item = None
        self.drag_start = (0, 0)
        self.drag_anchor = (0, 0)
    
    def wants_drag(self, x, y):
        return False
    
    def start_drag(self, x, y):
        return
    
    def continue_drag(self, x, y):
        return
    
    def end_drag(self, x, y):
        self.is_dragging_item = False
        if self.dragging_item:
            self.set_selected_item(self.dragging_item)
        self.dragging_item = False
    
    def has_selection(self):
        return self.selected_item is not None
    
    def update_item_from_inspector(self, widget=None):
        pass
    
    def update_inspector_from_item(self, widget=None):
        pass
    
    def set_selected_item(self, new_obj):
        # All the complex logic here is just to deal with the fact that sometimes
        # the new or old value will be None, so sometimes the associated inspector
        # will be hidden and therefore its fields will be inaccessible.
        old_obj = self.selected_item
        if old_obj is not None and new_obj is None:
            self.update_item_from_inspector()
            self.selected_item = new_obj
            self.inspector.hide()
            gamestate.main_window.pop_handlers()
        else:
            if old_obj is None and new_obj is not None:
                self.inspector.show()
                self.selected_item = new_obj
                self.update_inspector_from_item()
                gamestate.main_window.push_handlers(self.inspector)
            elif new_obj != old_obj:
                print 'y'
                self.update_item_from_inspector()
            if old_obj:
                self.selected_item = new_obj
                self.update_inspector_from_item()
    
