from engine import Engine


def setup():
    size(1280, 720)
    fill(255)
    noStroke()

    global e
    e = Engine()
    e.start()


def draw():
    background(0)

    global e
    e.tick()
    e.draw()


def stop():
    e.stop()
