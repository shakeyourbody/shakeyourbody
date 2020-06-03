import arcade
import csv
import math

from .events import mapped

from view import View
from pools import DataPool, EventsPool
from drawables import Circle
from animation import animate
from pose.sprited_pose import Pose
from utils.types import Point
from data.graphic.sprites import JOINTS_SPRITES
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

        self.clock = 0
        self.pclock = self.clock

        self.joints = None
        self.joints_sprites = None

        self.LOADED = False

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

        self.song = arcade.Sound(str(data.DATA_PATH / 'audio' / 'sample.mp3'))

        self.LOADED = True

    def __keypoint_handler(self, keypoint):
        x, y = keypoint
        self.keypoints.append(
            AnimatedCircle(x, y, 40, ttl=2).fill(245, 245, 245)
        )

    def on_show(self):
        arcade.set_background_color((15, 15, 15))
        self.song.play(volume=0.2)

    def on_update(self, arcade_elapsed):

        self.clock = self.song.get_stream_position()
        elapsed = self.clock - self.pclock
        self.pclock = self.clock

        self.keypoints_spawner.update(elapsed)
        self.keypoints = self.keypoints.filter(
            lambda keypoint: keypoint.update(elapsed))

        self.joints_sprites, self.joints = self.pose.joints()

    def on_draw(self):
        arcade.start_render()
        self.keypoints.each(lambda keypoint: keypoint.draw())

        if self.joints is None or self.joints_sprites is None:
            return

        for joint, sprite in self.joints_sprites.items():
            if sprite.center_x != 0 and sprite.center_y != 0:
                sprite.draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)

    def goto(self, *args):
        self.song.stop()
        super().goto(*args)
