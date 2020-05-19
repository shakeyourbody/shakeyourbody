from timedEvent import Pool, Frame, Event
from fake_pose import Pose
from drawables import Circle, Line, Text
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

        @thread
        def cbk():
            start = time()
            while time() - start < 1 and self.running:
                self._objs = {
                    'a': Circle(x1, y1, 20 - (time() - start)
                                * 18).fill(255, 0, 0),
                    'b': Circle(x2, y2, 20 - (time() - start)
                                * 18).fill(255, 0, 0),
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
        ]

        if 'a' in self._objs and 'b' in self._objs:
            self._dobj += [
                Line(ha, (self._objs['a'].x, self._objs['a'].y)).stroke(
                    255, 255, 255, 100),
                Line(hb, (self._objs['b'].x, self._objs['b'].y)).stroke(
                    255, 255, 255, 100)
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
