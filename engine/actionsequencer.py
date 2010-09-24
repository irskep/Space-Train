import collections

class ActionSequencer(object):
    """
    Action sequences consist of a list of lists of tuples. Like this:
    [   # Sequence of actions
        [   # Actions to perform simultaneously
            (function_to_call, (positional_arguments_to_function))
        ]
    ]
    
    This function, next_action(), pops an action off the front of the list and starts it.
    The actions themselves are responsible for calling next_action() when they are finished.
    
    Example:
    [
        [
            (move_to, ((10, 10), 'walk_left')),
            (scale_between, (0.5, 2.0, 2.0)),   #imaginary: scale_between(start, end, duration)
        ], 
        [
            (next_action, ())
        ]
    ]
    In this example, the ActionSequencer will (move from its current position to the point (10, 10))
    while (scaling between half and double size over a duration of two seconds). It will
    be up to move_to() and/or scale_between() to cause next_action() to be called at some
    point, either by setting done_function on an Interpolator or by setting a pyglet timer.
    """
    
    def __init__(self):
        self.actions = collections.deque()
        self.blocking_actions = 0
    
    def block(self):
        self.blocking_actions += 1
    
    def unblock(self):
        if self.blocking_actions > 0:
            self.blocking_actions -= 1
    
    def simple_sequence(self, *args):
        for func in args:
            self.actions.append([(func, [])])
        self.next_action()
    
    def next_action(self, ending_action=None):
        """Start the next action in the queue"""
        self.unblock()
        if len(self.actions) > 0:
            action_list = self.actions.popleft()
            self.block()
            for action in action_list:
                # Call first item (a function) in the action tuple with the parameters listed
                # as the second item in the tuple
                # Example: (move_to, ((x, y), 'walk_right'))
                action[0](*action[1])
    

