import arcade
import csv
import math

from .events import mapped

from view import View
from drawables import Circle, Text
from pools import DataPool, EventsPool
from pose.openpose import Pose
import data


class Playground(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)
        self.joints = DataPool()

    def setup(self):
        self.pose.connect()
        self.joints_sprites = dict(
            nose=arcade.Sprite(data.DATA_PATH/'graphic' /
                               'sprites'/'nose'/'nose.png', 0.04)
        )

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        coords, _ = self.pose.pose
        if coords is None:
            return

        x, y = coords['Nose']
        self.joints_sprites['nose'].center_x = self.width - self.width * x
        self.joints_sprites['nose'].center_y = self.height - \
            self.height * y * 2

        self.joints.clear()
        for joint in coords:
            x, y = coords[joint]
            if joint != 'Nose' and x != 0 and y != 0:
                x = self.width - self.width * x
                y = self.height - self.height * y * 2
                self.joints.append(Circle(x, y, 10).fill(245, 245, 245, 10))
                self.joints.append(Text(joint, x, y).fill(220, 220, 220))

    def on_draw(self):
        arcade.start_render()
        self.joints_sprites['nose'].draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)
