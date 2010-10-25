import pyglet, yaml

l = None
slides = []
slide_number = 0

def init(myscene):
    global l, slides
    slides = yaml.load(pyglet.resource.file(myscene.resource_path('slides.yaml'), 'r'))
    l = pyglet.text.Label(text=slides[0], x=200, y=520, width=880, height=320, 
                         font_name="Gill Sans", font_size=36, color=(255,0,255,255),
                         multiline=True, batch=myscene.batch)

def advance():
    global slide_number
    slide_number = (slide_number + 1) % len(slides)
    l.text = slides[slide_number]
