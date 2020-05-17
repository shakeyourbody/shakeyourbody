from timedStream import TimedStream, csv
import time

t = TimedStream(0)


def setup():
    size(400, 400)

    with open('data/colors.csv') as colors:
        reader = csv.reader(colors, delimiter=',')
        for timestamp, scale in reader:
            t.at(float(timestamp), float(scale))

    t.start()


def draw():
    bc = t()
    background(bc)
    if (len(t) <= 0):
        delay(1000)
        t.stop()
        exit()
