import os, pyglet, json

import settings, gamestate, util

class Environment(object):
    def __init__(self, name):
        self.name = name
        info_path = util.respath('environments', name, 'info.json')
        with pyglet.resource.file(info_path, 'r') as info_file:
            info = json.load(info_file)
            self.background_tile_rows = info['tile_rows']
            self.background_tile_cols = info['tile_columns']
        self.background_batch = pyglet.graphics.Batch()
        self.background_sprites = []
        self.width = 0
        self.height = 0
        background_sprites_dict = {}
        for x in range(self.background_tile_cols):
            for y in range(self.background_tile_rows):
                img = pyglet.resource.image(util.respath('environments', 
                                                         name, 
                                                         '%d_%d.png' % (x, y)))
                new_sprite = pyglet.sprite.Sprite(img, x=0, y=0, batch=self.background_batch)
                self.background_sprites.append(new_sprite)
                background_sprites_dict[(x, y)] = new_sprite
        for x in range(self.background_tile_cols):
            self.width += background_sprites_dict[(x, 0)].width
        for y in range(self.background_tile_rows):
            self.height += background_sprites_dict[(0, y)].height
        gamestate.camera_max = (self.width-gamestate.norm_w//2, self.height-gamestate.norm_h//2)
    
    def draw(self):
        self.background_batch.draw()
    
    def exit(self):
        for background_sprite in self.background_sprites:
            background_sprite.delete()
    
    def __repr__(self):
        return 'Environment(name="%s")' % self.name
    

        