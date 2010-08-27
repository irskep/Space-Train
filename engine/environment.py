import os, pyglet, json

import settings

class Environment(object):
    def __init__(self, name):
        self.name = name
        with open(os.path.join(settings.resources_path, 'environments', name, 'info.json'), 'r') as info_file:
            info = json.load(info_file)
            self.background_tile_rows = info['tile_rows']
            self.background_tile_cols = info['tile_columns']
        self.background_batch = pyglet.graphics.Batch()
        self.background_sprites = []
        for x in range(self.background_tile_cols):
            for y in range(self.background_tile_rows):
                img = pyglet.resource.nested_image('environments', 
                                                   name, 
                                                   '%d_%d.png' % (x, y))
                new_sprite = pyglet.sprite.Sprite(img, x=0, y=0, batch=self.background_batch)
                self.background_sprites.append(new_sprite)
    
    def draw(self):
        self.background_batch.draw()
    
    def exit(self):
        for background_sprite in self.background_sprites:
            background_sprite.delete()
    

        