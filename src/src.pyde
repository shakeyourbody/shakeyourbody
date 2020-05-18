from timedEvent import Event, Pool, Frame
import csv

f = Frame(0)
p = Pool()


def setup():
    size(400, 400)

    with open('data/colors.csv') as colors:
        reader = csv.reader(colors, delimiter=',')
        for timestamp, scale in reader:
            p.at(float(timestamp), Frame.cbk(float(scale)), f)

    p.start()


def draw():
    background(f.v)


def stop():
    p.stop()
