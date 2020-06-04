from time import time
import arcade
import csv

from .events import mapped, save, to_menu

from view import View
from pools import DataPool
from drawables import Circle
from animation import animate
from pose.sprited_pose import Pose
from utils.types import Point, filetypes
from utils.dialogs import openfile
import data


class Register(View):

    def __init__(self, WIDTH, HEIGHT, song_path, joints_format=['Nose', 'LWrist', 'RWrist']):
        super().__init__(WIDTH, HEIGHT)
        self.pose = Pose(WIDTH, HEIGHT)

        self.keypoints = None
        self.joints_format = joints_format

        self.joints = None
        self.joints_sprites = None

        self.song_path = song_path
        self.song = None

        self.clock = 0
        self.pclock = self.clock

        self.LOADED = False

    def setup(self):
        self.song = arcade.Sound(self.song_path)
        self.pose.connect()
        self.keypoints = dict()
        self.LOADED = True

    def on_show(self):
        arcade.set_background_color((15, 15, 15))
        self.song.play(volume=0.2)
        self.prev_stream_position = -1

    def on_update(self, elapsed):
        self.clock = self.song.get_stream_position()
        if self.clock == 0 and self.prev_stream_position == 0:
            save(self)
            to_menu(self)
        else:
            self.prev_stream_position = self.clock

        self.joints_sprites, self.joints = self.pose.joints()
        coords, _ = self.pose.pose
        if coords is None:
            return

        for joint in self.joints_format:
            if joint in coords:
                if not joint in self.keypoints:
                    self.keypoints[joint] = DataPool()
                self.keypoints[joint].append(
                    (self.clock, coords[joint]))

    def on_draw(self):
        arcade.start_render()

        # Time bar
        width = self.width * self.clock / self.song.get_length()
        height = 10
        arcade.draw_xywh_rectangle_filled(
            0, self.height - height,
            width, height,
            (245, 245, 245)
        )

        # joints stuff
        if self.joints is None or self.joints_sprites is None:
            return

        for joint, sprite in self.joints_sprites.items():
            if sprite.center_x != 0 and sprite.center_y != 0:
                sprite.draw()
        self.joints.each(lambda joint: joint.draw())

    def on_key_press(self, key, _):
        if key in mapped:
            mapped[key](self)

    def goto(self, *args):
        self.song.stop()
        super().goto(*args)
