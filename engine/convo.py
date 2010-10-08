import pyglet, json

import cam

from util import draw

class Conversation(object):
    def __init__(self, scn):
        super(Conversation, self).__init__()
        self.scene = scn
        
        self.convo_name = None
        self.convo_info = None
        self.animations = None
        self.remaining_convo_lines = None
        self.convo_label = pyglet.text.Label("", color = (0,0,0,255), 
                                             font_size=12, anchor_x='center')
    
    def active(self):
        return self.convo_name is not None
    
    def on_mouse_release(self, x, y, button, modifiers):
        if self.active():
            self.scene.clock.unschedule(self.next_line)
            self.next_line()
    
    def draw(self):
        if self.convo_label.text:
            draw.set_color(1,1,1,1)
            rect_args = (self.convo_label.x - self.convo_label.content_width/2 - 5, 
                         self.convo_label.y - 8,
                         self.convo_label.x + self.convo_label.content_width/2 + 10,
                         self.convo_label.y + self.convo_label.content_height + 3)
            draw.rect(*rect_args)
            draw.set_color(0,0,0,1)
            draw.rect_outline(*rect_args)
            self.convo_label.draw()
    
    def begin_conversation(self, convo_name):
        # Optimization: preload conversations in initializer
        self.convo_name = convo_name
        with pyglet.resource.file(self.scene.resource_path("%s.convo" % convo_name), 'r') as f:
            self.convo_info = json.load(f)
            self.animations = self.convo_info
            
            self.remaining_convo_lines = self.convo_info['start']
            self.next_line()
    
    def next_line(self, dt=0):
        if len(self.remaining_convo_lines) == 0:
            self.stop_speaking()
        else:
            command_or_actor = self.remaining_convo_lines[0][0]
            arg = self.remaining_convo_lines[0][1]
            if command_or_actor == 'goto':
                self.remaining_convo_lines = self.convo_info[arg]
                self.next_line()
            elif command_or_actor == 'choice':
                self.clear_speech_bubble()
                def decision_maker(goto):
                    def decision():
                        self.remaining_lines = self.convo_info[goto]
                        self.next_line()
                    return decision
                
                self.scene.ui.show_cam(self.scene.actors['main'], 
                                       {k: decision_maker(v) for k, v in arg.viewitems()})
            else:
                self.speak()
    
    def speak(self, dt=0):
        line = self.remaining_convo_lines[0]
        self.remaining_convo_lines = self.remaining_convo_lines[1:]
    
        actor_id = line[0]
        text = line[1]
        if len(line) == 3:
            temp_info = line[2]
            self.animations.update(temp_info)
        else:
            temp_info = None
        
        for identifier, new_state in self.animations['at_rest'].viewitems():
            if identifier != actor_id:
                self.scene.actors[identifier].update_state(new_state)
        act = self.scene.actors[actor_id]
        act.update_state(self.animations['speaking'][actor_id])
        self.convo_label.begin_update()
        self.convo_label.x = act.sprite.x
        self.convo_label.y = act.sprite.y + 20 + \
                             act.current_image().height - act.current_image().anchor_y
        self.convo_label.text = text
        self.convo_label.end_update()
        
        if temp_info:
            if temp_info.has_key('action'):
                getattr(act, temp_info['action'])()
    
        self.scene.clock.schedule_once(self.next_line, max(len(text)*0.04, 2.0))
    
    def clear_speech_bubble(self):
        self.convo_label.begin_update()
        self.convo_label.text = ""
        self.convo_label.end_update()
    
    def stop_speaking(self, dt=0):
        cn = self.convo_name
        self.convo_name = None  # Order matters here in case the script starts a new conversation
        self.convo_info = None
        self.animations = None
        self.scene.call_if_available('end_conversation', cn)
    
