import arcade
import csv
import math

from .events import mapped

from view import View
from drawables import Circle, Text
from pools import DataPool, EventsPool
from pose.openpose import Pose
from data.graphic.sprites import JOINTS_SPRITES
import data


class Playground(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)
        self.joints = DataPool()
        self.joints_sprites = JOINTS_SPRITES

    def setup(self):
        self.pose.connect()

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, elapsed):
        coords, _ = self.pose.pose
        if coords is None:
            return

        self.joints.clear()
        for joint in coords:
            x, y = coords[joint]
            if x != 0 and y != 0:
                x = self.width - self.width * x
                y = self.height - self.height * y * 2
                if joint in self.joints_sprites:
                    self.joints_sprites[joint].center_x = x
                    self.joints_sprites[joint].center_y = y
                else:
                    self.joints.append(
                        Circle(x, y, 10).fill(245, 245, 245, 10))
                    self.joints.append(Text(joint, x, y).fill(220, 220, 220))

    def on_draw(self):
        arcade.start_render()
        for joint, sprite in self.joints_sprites.items():
            if sprite.center_x != 0 and sprite.center_y != 0:
                sprite.draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)
