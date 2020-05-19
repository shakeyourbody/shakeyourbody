from timedEvent import Pool
from fake_pose import Pose
from drawables import Circle, Line, Text
from utils import Point

from time import time
import csv
import math


class Engine:

    def __init__(self):

        self.running = False

        self.pool = Pool()
        self.pose = Pose()

        self.TIMETOJUMP = 1

        self._dbuffer = []
        self._dmap = dict()

    def start(self):

        self.pool.clear()
        with open('data/moves.csv') as moves:
            reader = csv.reader(moves, delimiter=',')
            for timestamp, xa, ya, xb, yb in reader:
                self.pool.at(
                    float(timestamp) - self.TIMETOJUMP, self._handler,
                    Point(float(xa), float(ya)), Point(float(xb), float(yb))
                )
        self.pool.on('end', self._end_handler)
        self.pool.start()

        self.running = True

    def _handler(self, ea, eb):
        ra, rb = self.pose.pose()

        @thread
        def animate():
            start = time()
            while time() - start < self.TIMETOJUMP and self.running:
                self._dmap = {
                    'a': Circle(ea.x, ea.y, 20 - (time() - start) * 20).fill(255, 0, 0),
                    'b': Circle(eb.x, eb.y, 20 - (time() - start) * 20).fill(255, 0, 0)
                }
            da = math.sqrt((ea.x-ra.x)**2 + (ea.y-ra.y)**2)
            db = math.sqrt((eb.x-rb.x)**2 + (eb.y-rb.y)**2)
            print(da, db)

    def _end_handler(self):
        @thread
        def cbk():
            delay(1000)
            self.running = False
            self._dmap = dict()
            self._dbuffer = [
                Text('END!', width/2, height/2)
            ]

    def tick(self):
        if not self.running:
            return

        self._dbuffer = []
        self._dmap = dict()

        a, b = self.pose.pose()
        self._dbuffer = [
            Circle(a.x, a.y, 10),
            Circle(b.x, b.y, 10)
        ]

        if 'a' in self._dmap and 'b' in self._dmap:
            self._dbuffer += [
                Line(a, (self._dmap['a'].x, self._dmap['a'].y)),
                Line(b, (self._dmap['b'].x, self._dmap['b'].y))
            ]

    def draw(self):
        for obj in self._dbuffer:
            obj.draw()

        for key in self._dmap:
            self._dmap[key].draw()
