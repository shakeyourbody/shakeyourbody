from timedEvent import Pool, Frame
import csv


class Engine:

    def __init__(self):
        self.f = Frame(0)
        self.p = Pool()

    def start(self):
        self.p.clear()
        with open('data/data.csv') as colors:
            reader = csv.reader(colors, delimiter=',')
            for timestamp, scale in reader:
                self.p.at(float(timestamp), Frame.cbk(float(scale)), self.f)
        self.p.start()

    def draw(self):
        circle(width/2, height/2, self.f.v)
