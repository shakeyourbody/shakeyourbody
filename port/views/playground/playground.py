import arcade
import csv
import math

from .events import mapped

from view import View
from drawables import Circle, Text
from pools import DataPool, EventsPool
from pose.sprited_pose import Pose
import data


class Playground(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)
        self.joints = None
        self.joints_sprites = None

    def setup(self):
        self.pose.connect()

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        self.joints_sprites, self.joints = self.pose.joints()

    def on_draw(self):
        arcade.start_render()
        if self.joints is None or self.joints_sprites is None:
            return

        for joint, sprite in self.joints_sprites.items():
            if sprite.center_x != 0 and sprite.center_y != 0:
                sprite.draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)
