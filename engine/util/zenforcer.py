import pyglet

class ZEnforcer(object):
    """Ensure that sprites maintain z-order based on some sort key"""
    def __init__(self, parent_group, sprite_iterator, sort_function):
        self.parent_group = parent_group
        self.sprite_iterator = sprite_iterator
        self.sort_function = sort_function
        self.groups = []
        self.highest_group = 0
    
    def init_groups(self):
        """Create layer groups, inject __above/__below instance variables"""
        sprites = list(self.sprite_iterator())
        self.groups = [pyglet.graphics.OrderedGroup(order=i, parent=self.parent_group) \
                       for i in xrange(len(sprites))]
        
        # Iterate closest to farthest sprite (bottom to top)
        sorted_sprites = sorted(sprites, self.sort_function)
        for i in xrange(len(sorted_sprites)):
            s = sorted_sprites[i]
            s.group = self.groups[i]
            s.__below = None  # Sprite drawn below this one (higher on screen)
            s.__above = None  # Sprite drawn above this one (lower on screen)
            if i > 0:
                s.__below = sorted_sprites[i-1]
            if i < len(sorted_sprites)-1:
                s.__above = sorted_sprites[i+1]
    
    def swap_sprite_up(self, s):
        # A
        # B
        # C <- being swapped up
        # D
        
        B = s.__above
        C = s
        D = s.__below
        if B:
            A = B.__above
        else:
            A = None
        
        if D:
            D.__above = B
        
        if B:
            B.__below = D
            B.__above = C
        
        if C:
            C.__below = B
            C.__above = A
        
        if A:
            A.__below = C
        
        g1, g2 = B.group, C.group
        B.group, C.group = g2, g1
    
    def update(self, dt=0):
        for s in self.sprite_iterator():
            if s.__above and s.__above.y > s.y:
                self.swap_sprite_up(s)
    
