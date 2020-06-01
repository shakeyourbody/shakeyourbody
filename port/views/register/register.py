from time import time
import arcade
import csv

from .events import mapped

from view import View
from pools import DataPool
from drawables import Circle
from animation import animate
from pose.openpose import Pose
from utils.types import Point
import data


@animate(Circle)
def AnimatedCircle(self, elapsed, remaining, original):
    self.r = 20 * remaining / original


class Register(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)
        self.keypoints = DataPool()
        self.dkeypoints = DataPool()

    def setup(self):
        self.pose.connect()
        self.keypoints.clear()
        self.start = time()

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        coords, new = self.pose.pose
        if not new or coords is None:
            return

        x, y = coords['Nose']
        self.keypoints.append((time() - self.start, x, y))
        self.dkeypoints.append(Circle(self.width - x * self.width, y *
                                      self.height, 5).fill(120, 120, 120))

    def on_draw(self):
        arcade.start_render()
        self.dkeypoints.each(lambda keypoint: keypoint.draw())

    def on_key_press(self, key, _):
        if key in mapped:
            mapped[key](self)
