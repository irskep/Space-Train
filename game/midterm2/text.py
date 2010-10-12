import pyglet, yaml

l1 = None
t1 = """Backgrounds"""


def init(myscene):
    global l1
    l1 = pyglet.text.Label(text=t1, x=350, y=675, width=600, height=5500, 
                          font_name="Helvetica", font_size=36, color=(0,0,0,255),
                          multiline=True, batch=myscene.batch)
