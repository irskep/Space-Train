import pyglet, yaml, collections, functools

import cam

from util import draw

nonedict = functools.partial(collections.defaultdict, lambda: None)

class Conversation(object):
    def __init__(self, scn):
        super(Conversation, self).__init__()
        self.scene = scn
        
        self.convo_name = None
        self.convo_info = None
        self.animations = None
        self.convo_lines = None
        self.convo_position = 0
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
            x = self.convo_label.x
            y = self.convo_label.y
            w = self.convo_label.content_width
            h = self.convo_label.content_height
            rect_args = (x - w/2 - 5,  y     - 8,
                         x + w/2 + 10, y + h + 3)
            draw.rect(*rect_args)
            draw.set_color(0,0,0,1)
            draw.rect_outline(*rect_args)
            self.convo_label.draw()
    
    def _update_anim_dict(self, newdict):
        for k in ['at_rest', 'speaking']:
            if newdict.has_key(k):
                self.animations[k].update(newdict[k])
    
    def _reset_at_rest(self, exclude=None):
        for identifier, new_state in self.animations['at_rest'].viewitems():
            if identifier != exclude:
                self.scene.actors[identifier].update_state(new_state)
    
    def begin_conversation(self, convo_name):
        # Optimization: preload conversations in initializer
        self.convo_name = convo_name
        with pyglet.resource.file(self.scene.resource_path("%s.convo" % convo_name), 'r') as f:
            self.convo_info = yaml.load(f)
            self.convo_info['variables'] = nonedict(self.convo_info['variables'])
            self.animations = {
                'at_rest': {
                    'main': 'stand_right'
                },
                'speaking': {
                    'main': 'talk_right'
                }
            }
            self._update_anim_dict(self.convo_info)
            
            self.convo_lines = self.convo_info['start']
            self.convo_position = 0
            self.next_line()
    
    def _parse_command_dict(self, tags):
        if tags['set_local']:
            self.convo_info['variables'].update(tags['set_local'])
        if tags['update_animations']:
            self._update_anim_dict(tags['update_animations'])
            self._reset_at_rest()
        if tags['goto']:
            self.convo_position = 0
            self.convo_lines = self.convo_info[tags['goto']]
            if self.scene.ui.cam:
                self.scene.ui.cam.set_visible(False)
        self.next_line()
    
    def _make_choice_callback(self, choice, choice_dict, tag_dict):
        def decision():
            tags = nonedict(tag_dict)
            if tags['hide_after_use']:
                del choice_dict[choice]
            self._parse_command_dict(tags)
        return decision
    
    def _enforce_choice_requirements(self, choices):
        temp_choices = choices.copy()
        for choice, tags in choices.viewitems():
            if tags.has_key('require'):
                if not self.convo_info['variables'][tags['require']]:
                    del temp_choices[choice]
        return temp_choices
    
    def next_line(self, dt=0):
        if self.convo_position >= len(self.convo_lines):
            self.stop_speaking()
        else:
            line = self.convo_lines[self.convo_position]
            self.convo_position += 1
            if isinstance(line, dict):
                self._parse_command_dict(nonedict(line))
            elif isinstance(line[0], dict):
                self._parse_command_dict(nonedict(line[0]))
            elif line[0] == 'choice':
                self.clear_speech_bubble()
                
                temp_choices = self._enforce_choice_requirements(line[1])
                choice_mappings = {k: self._make_choice_callback(k, line[1], v) for k, v
                                   in temp_choices.viewitems()}
                self.scene.ui.show_cam(self.scene.actors['main'], choice_mappings)
            else:
                self.speak(*line)
    
    def speak(self, actor_id, text, temp_info=None):
        self._reset_at_rest(exclude=actor_id)
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
        self.clear_speech_bubble()
        
        # Order matters here in case the script starts a new conversation
        cn = self.convo_name
        self.convo_name = None
        self.convo_info = None
        self.animations = None
        self.scene.call_if_available('end_conversation', cn)
    
