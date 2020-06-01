import arcade
import csv
import math

from .events import mapped

from view import View
from pools import DataPool, EventsPool
from drawables import Circle
from animation import animate
from pose.openpose import Pose
from utils.types import Point
import data


@animate(Circle)
def AnimatedCircle(self, elapsed, remaining, original):
    self.r = 40 * remaining / original


class Song(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)

        self.pose = Pose(WIDTH, HEIGHT)

        self.keypoints_spawner = EventsPool()
        self.keypoints = DataPool()
        self.disposables = DataPool()

    def setup(self):

        self.pose.connect()

        self.keypoints_spawner.clear()
        with open(data.DATA_PATH / 'auto.csv') as poses:
            reader = csv.reader(poses, delimiter=',')
            for timestamp, x, y, in reader:
                self.keypoints_spawner.at(
                    float(timestamp), self.__keypoint_handler,
                    Point(float(x) * self.width, float(y) * self.height)
                )

        # self.pose.wait()

    def __keypoint_handler(self, keypoint):
        x, y = keypoint
        self.keypoints.append(
            AnimatedCircle(x, y, 40, ttl=2).fill(245, 245, 245)
        )

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        self.keypoints_spawner.update(elapsed)
        self.keypoints = self.keypoints.filter(
            lambda keypoint: keypoint.update(elapsed))

        self.disposables.clear()
        coords, new = self.pose.pose
        if coords is None:
            return
        x, y = coords['Nose']

        self.disposables.append(
            Circle(self.width - x * self.width, self.height - y *
                   self.height, 10).fill(120, 120, 120)
        )

    def on_draw(self):
        arcade.start_render()
        self.keypoints.each(lambda keypoint: keypoint.draw())
        self.disposables.each(lambda drawables: drawables.draw())

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)
