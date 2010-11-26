import pyglet
from pyglet.gl import *

class ShadowManager(object):
    def __init__(self):
        super(ShadowManager, self).__init__()
        self.batch = pyglet.graphics.Batch()
        
        self.shadow_image = pyglet.resource.image('ui/shadow.png')
        
        self.group = pyglet.sprite.SpriteGroup(self.shadow_image.texture,
            blend_src=GL_SRC_ALPHA, blend_dest=GL_ONE_MINUS_SRC_ALPHA)
        
        self.rel_cache = {}
        self.targets = []
    
    def set_targets(self, new_targets):
        self.targets = new_targets
        num = len(self.targets)
        self.vertex_list = self.batch.add(4*num, GL_QUADS, self.group,
            'v2i', 'c4B', ('t3f', self.shadow_image.texture.tex_coords*num))
        for n in xrange(0, num):
            self.vertex_list.vertices[n*8:(n+1)*8] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.vertex_list.colors[n*16:(n+1)*16] = [255,255,255,255] * 4
    
    def rel_pos(self, img):
        try:
            img.width
        except AttributeError:
            img = img.frames[0].image
        if not self.rel_cache.has_key(img):
            w, h = self.shadow_image.width, self.shadow_image.height
            iw, ih = img.width, img.height
            scale = float(iw)/float(w)*0.8
            self.rel_cache[img] = (-w*scale*0.5, -h*scale*0.5, w*scale, h*scale)
        return self.rel_cache[img]
    
    def draw(self, dt=0):
        w, h = self.shadow_image.width,self.shadow_image.height
        verts, clrs = self.vertex_list.vertices, self.vertex_list.colors
        for n, t in enumerate(self.targets):
            rel_x, rel_y, ww, hh = self.rel_pos(t.image)
            x = t.x + rel_x
            y = t.y + rel_y
            verts[n*8:(n+1)*8] = map(int,[x,y,x+ww,y,x+ww,y+hh,x,y+hh])
        self.batch.draw()
        
        