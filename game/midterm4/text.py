import pyglet, yaml
from engine.gamestate import norm_w, norm_h
from engine.interpolator import LinearInterpolator, Linear2DInterpolator

myscene = None
title = None
body = None
slides = []
slide_number = 0

def init(scn):
    global title, body, slides, myscene
    myscene = scn
    slides = yaml.load(pyglet.resource.file(myscene.resource_path('slides.yaml'), 'r'))
    
    this_slide = slides[0]
    tx, ty = this_slide['title_pos']
    bx, by = this_slide['body_pos']
    title = pyglet.text.Label(text=this_slide['title_text'], x=norm_w*tx, y=norm_h*ty, 
                              font_name='Helvetica Bold', font_size=48, multiline=False,
                              anchor_x='left', batch=myscene.batch, color=(255,255,255,255))
    body = pyglet.text.Label(text=this_slide['body_text'], x=norm_w*bx, y=norm_h*by, 
                          width=1000, height=520, 
                          font_name="Helvetica", font_size=36, color=(255,255,255,255),
                          multiline=True, batch=myscene.batch,
                          anchor_x='left', anchor_y='top')

def advance():
    global slide_number
    slide_number += 1
    if slide_number >= len(slides):
        myscene.handler.notify(None)
        return
    
    this_slide = slides[slide_number]
    
    print 'slide', slide_number
    
    if this_slide.has_key('title_pos'):
        tx, ty = this_slide['title_pos']
        title.x, title.y = tx*norm_w, ty*norm_h
    
    if this_slide.has_key('body_pos'):
        bx, by = this_slide['body_pos']
        body.x, body.y = bx*norm_w, by*norm_h
    
    title.begin_update()
    if this_slide.has_key('title_text'):
        title.text = this_slide['title_text']
    else:
        title.text = ""
    title.end_update()
    
    body.begin_update()
    if this_slide.has_key('body_text'):
        body.text = this_slide['body_text']
    else:
        body.text = ""
    body.end_update()
    
    if this_slide.has_key('call'):
        globals()[this_slide['call']]()
