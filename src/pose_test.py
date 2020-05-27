from pose import Pose
from drawables import Text
from time import time
from timedEvent import Frame

p = Pose()

drawables = []


def setup():
    size(1280, 720)
    p.connect()


def draw():
    global drawables
    background(0)

    coords, new = p.pose
    if new:
        drawables = [Text(key, value.x, value.y)
                     for key, value in coords.items()
                     if value.x != 0 and value.y != 0]

    for drawable in drawables:
        drawable.draw()


def stop():
    p.stop()
