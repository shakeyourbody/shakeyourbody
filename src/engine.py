from timedEvent import Pool, animate, delayed
from pose import Pose
# from fake_pose import Pose
from drawables import Circle, Line, Text
from utils import Point

from time import time
import csv
import math


class Engine:

    TIMETOJUMP = 2

    def __init__(self):

        self.running = False

        self.pool = Pool()
        self.pose = Pose()

        self._dbuffer = []
        self._dmap = dict()

    def start(self):

        self.pose.connect()
        self.pose.mirror(width)

        self.pool.clear()
        with open('data/poses.csv') as moves:
            reader = csv.reader(moves, delimiter=',')
            for timestamp, x, y in reader:
                self.pool.at(
                    float(timestamp) - self.TIMETOJUMP, self._handler,
                    Point(float(x) * width, float(y) * height)
                )
        self.pool.on('end:ok', self._end_handler)

        self.waitPose()

        self.pool.start()
        self.running = True

    def waitPose(self):
        while self.pose.pose[0] is None:
            pass

    @animate(TIMETOJUMP)
    def _handler(self, events, kp):
        coords, _ = self.pose.pose
        x, y = coords['Nose']

        events.loop_if(lambda: self.running)

        @events.animation
        def on_animation(elapsed):
            self._dmap = {
                'keypoint': Circle(kp.x, kp.y, 40 - elapsed * 40).fill(0, 255, 0),
            }

        @events.then
        def on_end():
            delta = math.sqrt((kp.x-x)**2 + (kp.y-y)**2)
            print(delta)

    @delayed(TIMETOJUMP)
    def _end_handler(self):
        self.running = False
        self._dmap = dict()
        self._dbuffer = [Text('END!', width/2, height/2)]

    def tick(self):
        if not self.running:
            return

        self._dbuffer = []
        self._dmap = dict()

        coords, _ = self.pose.pose
        x, y = coords['nose']

        self._dbuffer = [
            Circle(x, y, 20).fill(255, 0, 0)
        ]

        if 'keypoint' in self._dmap:
            kp = self._dmap['keypoint']
            self._dbuffer += [Line((x, y), ((kp.x, kp.y)))]

    def stop(self):
        self.running = False
        self.pool.stop()
        self.pose.stop()

    def draw(self):
        for obj in self._dbuffer:
            obj.draw()

        for key in self._dmap:
            self._dmap[key].draw()
