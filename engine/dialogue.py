import pyglet, time, util
from time import clock

class Dialogue(object):
    def __init__ (self, main, other):
        self.main = main
        self.other = other
        self.target = self.main
        self.f = open("test.txt", 'r')
        self.line = self.f.readline()
        if self.line[0] == "m":
            self.target = self.main
        if self.line[0] == "o":
            self.target = self.other
        self.start = time.clock()
        self.label = pyglet.text.Label(self.f.readline(),
            color = (0,255,0,255),
            font_name='Comic Sans MS',
            font_size=12,
            x = self.target.sprite.x, y = self.target.sprite.y)

    def update(self):
        self.label.x = self.target.sprite.x - 30
        self.label.y = self.target.sprite.y + 200
        if(time.clock() - self.start > 2):
            self.line = self.f.readline()
            if self.line != "": 
                if self.line[0] == "m":
                    self.target = self.main
                    self.label.text = self.f.readline()
                if self.line[0] == "o":
                    self.target = self.other
                    self.label.text = self.f.readline()
                self.start = time.clock()
            else:
                self.label.text = ""

    def draw(self):
        self.label.draw()
