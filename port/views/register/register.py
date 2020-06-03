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
from utils.dialogs import openfile
from data.graphic.sprites import JOINTS_SPRITES
import data


class Register(View):

    def __init__(self, WIDTH, HEIGHT, joints_format=['Nose', 'LWrist', 'RWrist']):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)
        self.keypoints = None
        self.joints_sprites = JOINTS_SPRITES
        self.joints_format = joints_format

    def setup(self):
        self.pose.connect()
        self.keypoints = dict()
        self.start = time()

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        coords, new = self.pose.pose
        if not new or coords is None:
            return

        # formatted_keypoints = []
        # for joint in self.joints_format:
        #     if joint in coords:
        #         formatted_keypoints.append(coords[joint])
        # self.keypoints.append((time() - self.start, formatted_keypoints))
        now = round(time() - self.start, 3)
        for joint in self.joints_format:
            if joint in coords:
                if not joint in self.keypoints:
                    self.keypoints[joint] = DataPool()
                self.keypoints[joint].append(
                    (now, coords[joint]))

    def on_draw(self):
        arcade.start_render()

    def on_key_press(self, key, _):
        if key in mapped:
            mapped[key](self)
