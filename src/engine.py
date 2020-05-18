from timedEvent import Pool, Frame, Event
import csv


class Engine:

    def __init__(self):
        self.f = Frame(0)
        self.p = Pool()

    def start(self):
        self.p.clear()
        oub = (-100, -100, -100, -100)
        with open('data/moves.csv') as colors:
            reader = csv.reader(colors, delimiter=',')
            for timestamp, x1, y1, x2, y2 in reader:
                self.p.at(float(timestamp), Frame.cbk(
                    (float(x1), float(y1), float(x2), float(y2))), self.f)
        self.p.on('end', lambda: Event(1, lambda: self.f.set(oub)).start())
        self.p.start()

    def draw(self):
        if self.f.v == 0:
            return
        x1, y1, x2, y2 = self.f.v

        fill(150, 100, 250)
        circle(x1, y1, 10)
        circle(x2, y2, 10)
