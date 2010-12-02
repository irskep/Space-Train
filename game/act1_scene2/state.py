myscene = None

convo_handlers = {}

def handles_convo(*labels):
    def inner(f):
        for label in labels:
            convo_handlers[label] = f
        return f
    return inner

click_handlers = {}

def handles_click(*labels):
    def inner(f):
        for label in labels:
            click_handlers[label] = f
        return f
    return inner

walk_handlers = {}

def handles_walk(*labels):
    def inner(f):
        for label in labels:
            walk_handlers[label] = f
        return f
    return inner

transition_handlers = {}

def handles_transition(*labels):
    def inner(f):
        for label in labels:
            transition_handlers[label] = f
        return f
    return inner

    
def start_cutscene():
    myscene.interaction_enabled = False
    myscene.moving_camera = True
    
def end_cutscene():
    myscene.interaction_enabled = True
    myscene.moving_camera = False