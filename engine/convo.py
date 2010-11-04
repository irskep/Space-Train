"""
Cutscenes, mostly just 1-on-1 dialogue. This stuff is complicated, read carefully.

TODO:
- Preload conversations (make sure to *copy*, not *reference* convo_info)
"""

import pyglet, yaml, collections, functools
import actor
from util import draw

# Convenience function for creating defaultdicts that return None if key not present
nonedict = functools.partial(collections.defaultdict, lambda: None)

class Conversation(object):
    """
    Starts, runs, and stops cutscenes.
    
    The file format is JSON/YAML. Either syntax can be used, but YAML is easier on the eyes.
    
    A conversation file should reside in its scene's data folder and have the extension ".convo".
    At the top level, it is a dictionary with a few required keys and as many non-required keys
    as you desire.
    
    Required keys:
    
        # Animations
        at_rest:    # actor ID: image to show when actor is not speaking
            main: stand_right
            bean_salesman: stand_front
        
        speaking:   # actor ID: image to show when actor is speaking
            main: talk_right
            bean_salesman: stand_front
        
        variables:  # Variable name: initial value (can be updated with update_locals)
            bean_hate: false
            bean_interest: false
        
        # Dialogue entry point
        start:
            [action list]
    
    Action list format:
        - command: argument
        - command: argument
        - ...
    
    Commands:
        goto: <label>
            Start executing the action list under the top-level label <label>
            
            EXAMPLE: goto start
        
        actor_id: <text>
            Make an actor speak a phrase. Delay the next action.
            
            EXAMPLE:
                bean_salesman: What a nice day it is today!
        
        actor_id: <dictionary>
            Perform actions on one actor. Currently only accepts one key:
                action: <action_name>
                    Calls actor.action_name()
            
            EXAMPLE:
                bean_salesman:
                    action: jump
        
        update_locals:
            name: value
            name: value
            ...
            
            Set/update the values of any conversation-local variables
        
        choice:
            <choice text>:
                [action list]
            <another choice>:
                [action list]
            
            Present a contextual action menu to the user with dialogue options.
            
            The action list accepts two extra commands:
                hide_after_use: true
                    Do not show this choice again in this conversation.
                require: <local>
                    Require that the conversation variable <local> be set to some true value
            
            (hide_after_use is somewhat redundant to update_locals+require, but it's convenient.)
    """
    def __init__(self, scn):
        super(Conversation, self).__init__()
        self.scene = scn
        
        self.convo_name = None
        self.convo_info = None
        self.animations = None
        self.convo_lines = None
        self.convo_position = 0
        
        self.convo_label = pyglet.text.Label("", color = (0,0,0,255), font_size=12, 
                                             anchor_x='center', anchor_y='bottom',
                                             multiline=True, width=400)
    
    def delete(self):
        self.convo_label.delete()
    
    active = property(lambda self: self.convo_name is not None)
    
    def on_mouse_release(self, x, y, button, modifiers):
        """Skip speaking delay on mouse click"""
        if self.active and not self.scene.ui.cam:
            self.scene.clock.unschedule(self.next_line)
            self.next_line()
    
    def draw(self):
        """Draw dialogue box and text"""
        if self.convo_label.text:
            draw.set_color(1,1,1,1)
            x = self.convo_label.x
            y = self.convo_label.y
            w = self.convo_label.content_width
            h = self.convo_label.content_height
            
            rect_args = (x - (400 / 2) - 5,  y - 5,
                         x + (400 / 2) + 5,  y + h + 5)

            draw.rect(*rect_args)
            draw.set_color(0,0,0,1)
            draw.rect_outline(*rect_args)
            self.convo_label.draw()
    
    def _update_anim_dict(self, newdict):
        """Update the animation mappings with new values from <newdict>"""
        for k in ['at_rest', 'speaking']:
            if newdict.has_key(k):
                self.animations[k].update(newdict[k])
    
    def _reset_at_rest(self, exclude=None):
        """Set all involved actors to their resting positions"""
        for identifier, new_state in self.animations['at_rest'].viewitems():
            if identifier != exclude:
                self.scene.actors[identifier].update_state(new_state)
    
    def begin_conversation(self, convo_name):
        """Start a cutscene named <convo_name>"""
        self.convo_name = convo_name
        with pyglet.resource.file(self.scene.resource_path("%s.convo" % convo_name), 'r') as f:
            self.convo_info = yaml.load(f)
            # Variables default to None
            self.convo_info['variables'] = nonedict(self.convo_info['variables'])
            # Bare minimum of animations
            self.animations = {
                'at_rest': {
                    'main': 'stand_right'
                },
                'speaking': {
                    'main': 'talk_right'
                }
            }
            # Add animations from YAML file
            self._update_anim_dict(self.convo_info)
            
            # Go!
            self.convo_lines = self.convo_info['start']
            self.convo_position = 0
            self.next_line()
    
    # ACTION LIST COMMANDS
    # Returns True if the caller can/should immediately execute the next line
    
    def _update_locals(self, val):
        """Update variables dictionary"""
        for val in v:
            self.convo_info['variables'].update(v)
        return True
    
    def _give(self, val):
        print 'give', val
        new_actor = self.scene.new_actor(val)
        self.scene.ui.inventory.put_item(new_actor)
        return True
    
    def _update_animations(self, val):
        """Update animations dictionary"""
        self._update_anim_dict(val)
        self._reset_at_rest()
        return True
    
    def _goto(self, val):
        """Start executing a different action list"""
        self.convo_position = 0
        self.convo_lines = self.convo_info[val]
        if self.scene.ui.cam:
            self.scene.ui.cam.set_visible(False)
        return True
    
    def _choice(self, val):
        """Present the user with a CAM where each button goes to a different label"""
        self.clear_speech_bubble()
        
        temp_choices = self._enforce_choice_requirements(val)
        choice_mappings = {k: self._make_choice_callback(k, val, v) for k, v
                           in temp_choices.viewitems()}
        self.scene.ui.show_cam(self.scene.actors['main'], choice_mappings)
        self.scene.ui.cam.hide_on_click_outside = False
        return False
    
    def _parse_command_dict(self, cmd_dict):
        """Search cmd_dict for actions to execute. Return True if caller should call next_line()."""
        needs_schedule = True
        for cmd, arg in cmd_dict.viewitems():
            try:
                result = getattr(self, '_%s' % cmd)(arg)
                needs_schedule = needs_schedule and result
            except AttributeError:
                pass    # Don't care, it's probably a spoken line
        return needs_schedule
    
    # CHOICE ACTION HELPERS
    
    def _make_choice_callback(self, choice, choice_dict, tag_dict):
        """Create a function to be called when a choice is clicked"""
        def decision():
            tags = nonedict(tag_dict)
            if tags['hide_after_use']:
                del choice_dict[choice]
            self._parse_command_dict(tags)
            self.next_line()
        return decision
    
    def _enforce_choice_requirements(self, choices):
        """Enforce 'requires' choice action"""
        temp_choices = choices.copy()
        for choice, tags in choices.viewitems():
            if tags.has_key('require'):
                if not self.convo_info['variables'][tags['require']]:
                    del temp_choices[choice]
        return temp_choices
    
    # OTHER CUTSCENE STUFF
    
    def next_line(self, dt=0):
        """Advance the cutscene by one line in the current action list"""
        if self.convo_position >= len(self.convo_lines):
            self.stop_speaking()
        else:    
            line = self.convo_lines[self.convo_position]
            self.convo_position += 1
            needs_schedule = self._parse_command_dict(nonedict(line))
            for actor_id, arg in line.viewitems():
                if self.scene.actors.has_key(actor_id):
                    self.speak(actor_id, arg)
                    needs_schedule = False
            if needs_schedule:
                self.next_line()
    
    def speak(self, actor_id, arg):
        """Actor-specific actions like speaking and jumping"""
        self._reset_at_rest(exclude=actor_id)
        act = self.scene.actors[actor_id]
        if isinstance(arg, str):
            act.update_state(self.animations['speaking'][actor_id])
            self.convo_label.begin_update()
            self.convo_label.x = act.sprite.x
            self.convo_label.y = act.sprite.y + 20 + \
                                 act.current_image().height - act.current_image().anchor_y
            self.convo_label.text = arg
            self.convo_label.end_update()
            self.scene.clock.schedule_once(self.next_line, max(len(arg)*0.05, 3.0))
        else:
            if arg.has_key('action'):
                getattr(act, arg['action'])()
                self.next_line()
    
    def clear_speech_bubble(self):
        """Clear all spoken text"""
        self.convo_label.begin_update()
        self.convo_label.text = ""
        self.convo_label.end_update()
    
    def stop_speaking(self, dt=0):
        """Stop the cutscene"""
        self.clear_speech_bubble()
        
        # Order matters here in case the script starts a new conversation
        cn = self.convo_name
        self.convo_name = None
        self.convo_info = None
        self.animations = None
        self.scene.call_if_available('end_conversation', cn)
    
