import pyglet, yaml

l1 = None
t1 = """Environment
  • Background
  • Scripted NPCs (cart lady)
  • Walking"""

l2 = None
t2 = """Conversations"""


def init(myscene):
    global l1
    l1 = pyglet.text.Label(text=t1, x=350, y=675, width=600, height=5500, 
                          font_name="Helvetica", font_size=36, color=(0,0,0,255),
                          multiline=True, batch=myscene.batch)
    
    l2 = pyglet.text.Label(text=t2, x=1500, y=675, width=600, height=5500, 
                          font_name="Helvetica", font_size=36, color=(0,0,0,255),
                          multiline=True, batch=myscene.batch)
