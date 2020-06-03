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

        self.joints_sprites = JOINTS_SPRITES

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
        self.song.play(volume=0.2)

    def __keypoint_handler(self, keypoint):
        x, y = keypoint
        self.keypoints.append(
            AnimatedCircle(x, y, 40, ttl=2).fill(245, 245, 245)
        )

    def on_show(self):
        arcade.set_background_color((15, 15, 15))

    def on_update(self, arcade_elapsed):

        self.clock = self.song.get_stream_position()
        elapsed = self.clock - self.pclock
        self.pclock = self.clock

        self.keypoints_spawner.update(elapsed)
        self.keypoints = self.keypoints.filter(
            lambda keypoint: keypoint.update(elapsed))

        coords, new = self.pose.pose
        if coords is None or not new:
            return

        x, y = coords['Nose']
        self.joints_sprites['nose'].center_x = self.width - self.width * x
        self.joints_sprites['nose'].center_y = self.height - \
            self.height * y * 2     # TODO: fix camera proportions

    def on_draw(self):
        arcade.start_render()
        self.keypoints.each(lambda keypoint: keypoint.draw())
        self.joints_sprites['nose'].draw()

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)

    def goto(self, *args):
        self.song.stop()
        super().goto(*args)
