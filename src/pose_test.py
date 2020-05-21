from pose import Pose
from drawables import Circle, Text
from time import time
from timedEvent import Frame

p = Pose()
c = Circle(1280/2, 720/2, 10)

t = Text('none', 30, 20)

start = Frame(time())


def setup():
    size(1280, 720)
    p.connect()


def draw():
    background(0)

    coords, new = p.pose
    if new:
        nose = coords['nose']
        c.x = 1280 - nose.x
        c.y = nose.y

        t.s = 1/(time() - start.v)
        start.set(time())

    c.draw()
    t.draw()


def stop():
    p.stop()
