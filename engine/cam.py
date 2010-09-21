"""
File:           cam.py
Author:         Fred Hatfull
Description:    A class encompassing the primary functionality of the Contextual Action Menu (CAM) in SPACE TRAIN.
Notes: 

Contextual Action Menu Life Cycle:
* A CAM instance is requested by a caller (scene, object, level script, something)
    * The caller must provide:
        + A reference to the UI object in use (will probably be a singleton/global)
        + A dictionary of available actions: {'action_name': [function or closure]}
        + A coordinate indicating the centre of menu area around which actions will appear
* A CAM is instantiated and attached to the UI object
* The CAM is set to visible to indicate that it should drawn by the UI each frame at the specified coordinates
* The CAM remains visible until it detects a click:
    * If the click is within a region controlled by the CAM (i.e. on an action button), the CAM calls the callback associated with the action
    * If the click is elsewhere, pass the event down the event stack and set the CAM to false.
        * Destroy the CAM instance?

"""

import UI

class CAM(object):
    
    # Init
    def __init__(self, ui):
        self.visible = False
        ui.cam = self
        