from engine import Engine

e = Engine()


def setup():
    size(400, 400)
    fill(255)
    noStroke()
    e.start()


def draw():
    background(0)
    e.tick()
    e.draw()


def stop():
    e.pool.stop()
