from timedEvent import Pool, Frame, Event
from fake_pose import Pose
from time import time
import csv
import math


class Engine:

    def __init__(self):

        self.running = False

        self.p = Pool()
        self.poses = Pose()

        self._dobj = []
        self._objs = dict()

    def start(self):
        self.p.clear()
        with open('data/moves.csv') as colors:
            reader = csv.reader(colors, delimiter=',')
            for timestamp, x1, y1, x2, y2 in reader:
                self.p.at(float(timestamp) - 1, self._handle,
                          float(x1), float(y1), float(x2), float(y2))
        self.p.on('end', self.end)
        self.p.start()
        self.running = True

    def _handle(self, x1, y1, x2, y2):
        ha, hb = self.poses.pose()
        self._objs = dict(
            a=Circle(x1, y1, 10, fill=(255, 0, 0)),
            b=Circle(x2, y2, 10, fill=(255, 0, 0)),
        )

        @thread
        def cbk():
            start = time()
            while time() - start < 1 and self.running:
                self._objs = {
                    'a': Circle(x1, y1, 20 - (time() - start)
                                * 18, fill=(255, 0, 0)),
                    'b': Circle(x2, y2, 20 - (time() - start)
                                * 18, fill=(255, 0, 0)),
                }
            da = math.sqrt((x1-ha[0])**2 + (y1-ha[1])**2)
            db = math.sqrt((x2-hb[0])**2 + (y2-hb[1])**2)
            print(da, db)
            self._objs = dict()

    def tick(self):
        if not self.running:
            return

        ha, hb = self.poses.pose()

        self._dobj = [
            Circle(ha[0], ha[1], 10),
            Circle(hb[0], hb[1], 10),
            Line(ha, (self._objs['a'].x, self._objs['a'].y)
                 ) if 'a' in self._objs else Drawable(),
            Line(hb, (self._objs['b'].x, self._objs['b'].y)
                 ) if 'b' in self._objs else Drawable(),
        ]

    def draw(self):
        background(0)
        for key in self._objs:
            self._objs[key].draw()
        for el in self._dobj:
            el.draw()

    def end(self):
        @thread
        def cbk():
            delay(1000)
            self.running = False
            self._objs = dict()
            self._dobj = [
                Text('END!', width/2, height/2)
            ]


class Circle:

    def __init__(self, x, y, r, fill=(255, 255, 255)):
        self.x = x
        self.y = y
        self.r = r
        self.f = fill

    def draw(self):
        fill(*self.f)
        circle(self.x, self.y, self.r)


class Line:

    def __init__(self, a, b, stroke=(255, 255, 255, 100)):
        self.a = a
        self.b = b
        self.s = stroke

    def draw(self):
        stroke(*self.s)
        line(self.a[0], self.a[1], self.b[0], self.b[1])
        noStroke()


class Text():

    def __init__(self, s, x, y, fill=(255, 255, 255)):
        self.s = s
        self.x = x
        self.y = y
        self.f = fill

    def draw(self):
        fill(*self.f)
        textAlign(CENTER, CENTER)
        text(self.s, self.x, self.y)


class Drawable():
    def draw(self):
        pass
