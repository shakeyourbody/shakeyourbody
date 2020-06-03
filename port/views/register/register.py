from time import time
import arcade
import csv

from .events import mapped

from view import View
from pools import DataPool
from drawables import Circle
from animation import animate
from pose.sprited_pose import Pose
from utils.types import Point
from utils.dialogs import openfile
import data


class Register(View):

    def __init__(self, WIDTH, HEIGHT, joints_format=['Nose', 'LWrist', 'RWrist']):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)

        self.keypoints = None
        self.joints_format = joints_format

        self.joints = None
        self.joints_sprites = None

    def setup(self):
        self.pose.connect()
        self.keypoints = dict()
        self.start = time()

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        self.joints_sprites, self.joints = self.pose.joints()

        coords, _ = self.pose.pose
        if coords is None:
            return

        now = round(time() - self.start, 3)
        for joint in self.joints_format:
            if joint in coords:
                if not joint in self.keypoints:
                    self.keypoints[joint] = DataPool()
                self.keypoints[joint].append(
                    (now, coords[joint]))

    def on_draw(self):
        arcade.start_render()

        if self.joints is None or self.joints_sprites is None:
            return

        for joint, sprite in self.joints_sprites.items():
            if sprite.center_x != 0 and sprite.center_y != 0:
                sprite.draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, _):
        if key in mapped:
            mapped[key](self)
