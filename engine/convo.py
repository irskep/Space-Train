import pyglet, json

class Conversation(object):
    def __init__(self, scn):
        super(Conversation, self).__init__()
        self.scene = scn
        
        self.convo_name = None
        self.convo_info = None
        self.remaining_convo_lines = None
        self.convo_label = pyglet.text.Label("", color = (0,255,0,255), 
                                             font_size=12, anchor_x='center')
    
    def active(self):
        return self.convo_name is not None
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.active():
            self.scene.clock.unschedule(self.speak)
            self.speak()
    
    def draw(self):
        self.convo_label.draw()
    
    def begin_conversation(self, convo_name):
        # Optimization: preload conversations in initializer
        self.convo_name = convo_name
        with pyglet.resource.file(self.scene.resource_path("%s.convo" % convo_name), 'r') as f:
            self.convo_info = json.load(f)
        
        self.remaining_convo_lines = self.convo_info['dialogue']
        self.speak()
    
    def speak(self, dt=0):
        if len(self.remaining_convo_lines) == 0:
            self.stop_speaking()
        else:
            line = self.remaining_convo_lines[0]
            self.remaining_convo_lines = self.remaining_convo_lines[1:]
        
            actor_id = line[0]
            text = line[1]
            if len(line) == 3:
                self.convo_info = line[2]
            for identifier, new_state in self.convo_info['at_rest'].viewitems():
                if identifier != actor_id:
                    self.scene.actors[identifier].update_state(new_state)
            act = self.scene.actors[actor_id]
            act.update_state(self.convo_info['speaking'][actor_id])
            self.convo_label.begin_update()
            self.convo_label.x = act.sprite.x
            self.convo_label.y = act.sprite.y + 20 + \
                                 act.current_image().height - act.current_image().anchor_y
            self.convo_label.text = text
            self.convo_label.end_update()
        
            self.scene.clock.schedule_once(self.speak, max(len(text)*0.04, 2.0))
    
    def stop_speaking(self, dt=0):
        self.convo_label.begin_update()
        self.convo_label.text = ""
        self.convo_label.end_update()
        cn = self.convo_name
        self.convo_name = None  # Order matters here in case the script starts a new conversation
        self.convo_info = None
        self.scene.call_if_available('end_conversation', cn)
        