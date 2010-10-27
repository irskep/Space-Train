import os, pyglet, json

import gamestate, util

class Environment(object):
    def __init__(self, name, group=None):
        self.name = name
        info_path = util.respath('environments', name, 'info.json')
        with pyglet.resource.file(info_path, 'r') as info_file:
            info = json.load(info_file)
            self.background_tile_rows = info['tile_rows']
            self.background_tile_cols = info['tile_columns']
        self.background_batch = pyglet.graphics.Batch()
        self.background_sprites = []
        self.overlay_batch = pyglet.graphics.Batch()
        self.overlay_sprites = []
        
        self.width = 0
        self.height = 0
        background_sprites_dict = {}
        tile_w = 0
        tile_h = 0
        for x in range(self.background_tile_cols):
            this_y = 0
            for y in range(self.background_tile_rows):
                img = pyglet.resource.image(util.respath('environments', 
                                                         name, 
                                                         '%d_%d.png' % (x, y)))
                tile_w, tile_h = img.width, img.height
                new_sprite = pyglet.sprite.Sprite(img, x=x*tile_w, y=y*tile_h,
                                                  batch=self.background_batch,
                                                  group=group)
                self.background_sprites.append(new_sprite)
                background_sprites_dict[(x, y)] = new_sprite
        for x in range(self.background_tile_cols):
            self.width += background_sprites_dict[(x, 0)].width
        for y in range(self.background_tile_rows):
            self.height += background_sprites_dict[(0, y)].height
        gamestate.camera_max = (self.width-gamestate.norm_w//2, self.height-gamestate.norm_h//2)
        
        for x in range(self.background_tile_cols):
            for y in range(self.background_tile_rows):
                overlay_tile_path = util.respath('environments', name, 'overlay_%d_%d.png' % (x, y))
                try:
                    img = pyglet.resource.image(overlay_tile_path)
                    new_sprite = pyglet.sprite.Sprite(img, x=x*tile_w, y=y*tile_h,
                                                      batch=self.overlay_batch)
                    print new_sprite
                    self.overlay_sprites.append(new_sprite)
                except pyglet.resource.ResourceNotFoundException:
                    pass    # Ignore if no overlay
        
        self.draw = self.background_batch.draw
        self.draw_overlay = self.overlay_batch.draw
    
    def exit(self):
        for background_sprite in self.background_sprites:
            background_sprite.delete()
    
    def __repr__(self):
        return 'Environment(name="%s")' % self.name