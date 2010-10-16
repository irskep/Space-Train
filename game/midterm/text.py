import pyglet, yaml
from engine.gamestate import norm_w, norm_h
from engine.interpolator import LinearInterpolator, Linear2DInterpolator, PulseInterpolator

myscene = None
title = None
body = None
slides = []
slide_number = 0

pulse_interp = None

def init(scn):
    global title, body, slides, myscene, pulse_interp
    myscene = scn
    slides = yaml.load(pyglet.resource.file(myscene.resource_path('slides.yaml'), 'r'))
    
    logo = myscene.actors['logo']
    pulse_interp = PulseInterpolator(logo.sprite, 'scale', 0.95, 1.0, speed=4)
    myscene.add_interpolator(pulse_interp)
    
    myscene.actors['zeppelin_poster'].sprite.visible = False
    myscene.actors['train_poster'].sprite.visible = False
    
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
    slide_number = (slide_number + 1) % len(slides)
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

def hide_poster_show_stanislov():
    pulse_interp.stop = True
    logo = myscene.actors['logo']
    interp = LinearInterpolator(logo.sprite, 'scale', 1.5, duration=1.0)
    myscene.add_interpolator(interp)
    
    logo = myscene.actors['logo']
    interp = LinearInterpolator(logo.sprite, 'opacity', 0, 255, duration=1.0)
    myscene.add_interpolator(interp)
    
    stan = myscene.actors['stanislov']
    interp = Linear2DInterpolator(stan.sprite, 'position', (900, stan.sprite.y), speed=400.0)
    myscene.add_interpolator(interp)
    # myscene.actors['stanislov'].sprite.visible = True

def make_stanislov_big():
    stan = myscene.actors['stanislov']
    interp = Linear2DInterpolator(stan.sprite, 'position', (0, -800), duration=1.0)
    myscene.add_interpolator(interp)
    interp = LinearInterpolator(stan.sprite, 'scale', 4.8, duration=1.0)
    myscene.add_interpolator(interp)

def hide_stanislov_again():
    stan = myscene.actors['stanislov']
    interp = Linear2DInterpolator(stan.sprite, 'position', (stan.sprite.x, -2000), duration=1.0)
    myscene.add_interpolator(interp)

def kidnap():
    kidnapper = myscene.actors['kidnapper']
    interp = Linear2DInterpolator(kidnapper.sprite, 'position', (-200, kidnapper.sprite.y),
                                  speed=400)
    myscene.add_interpolator(interp)

def the_zeppelin():
    myscene.actors['zeppelin_poster'].sprite.visible = True

def the_baron():
    interp = LinearInterpolator(myscene.actors['zeppelin_poster'].sprite, 
                                'opacity', end=0, start=255, duration=1.0)
    myscene.add_interpolator(interp)
    baron = myscene.actors['baron_poster']
    interp = Linear2DInterpolator(baron.sprite, 'position', (baron.sprite.x, 360), duration=1.0)
    myscene.add_interpolator(interp)

def hide_baron():
    interp = LinearInterpolator(myscene.actors['baron_poster'].sprite, 
                                'opacity', end=0, start=255, duration=1.0)
    myscene.add_interpolator(interp)

def go_to_demo():
    myscene.handler.notify('midterm2')