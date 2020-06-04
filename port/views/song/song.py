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
from score import Score
from path import delta
import data


@animate(Circle)
def AnimatedCircle(self, elapsed, remaining, original):
    self.r = 5 * remaining / original


class Song(View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)

        self.pose = Pose(WIDTH, HEIGHT)
        self.score = Score()

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
        with open(data.DATA_PATH / 'registered' / 'moves.csv') as moves:
            reader = csv.reader(moves, delimiter=',')
            for row in reader:
                self.keypoints_spawner.at(
                    float(row[0]), self.__keypoint_handler, row[1:])

        with open(data.DATA_PATH / 'registered' / 'song.path') as song_path:
            self.song = arcade.Sound(song_path.read())

        self.LOADED = True

    def __keypoint_handler(self, keypoints):

        nosex = float(keypoints[0]) * self.width
        nosey = float(keypoints[1]) * self.height
        rwristx = float(keypoints[2]) * self.width
        rwristy = float(keypoints[3]) * self.height
        lwristx = float(keypoints[4]) * self.width
        lwristy = float(keypoints[5]) * self.height

        if nosex != 0 and nosey != 0:
            self.keypoints.append(AnimatedCircle(
                nosex, nosey, 40, ttl=0.5, on_end=self.__animation_end_handler, name='Nose').fill(245, 245, 245))

        if rwristx != 0 and rwristy != 0:
            self.keypoints.append(AnimatedCircle(
                rwristx, rwristy, 40, ttl=0.5, on_end=self.__animation_end_handler, name='RWrist').fill(245, 245, 245))

        if lwristx != 0 and lwristy != 0:
            self.keypoints.append(AnimatedCircle(
                lwristx, lwristy, 40, ttl=0.5, on_end=self.__animation_end_handler, name='LWrist').fill(245, 245, 245))

    def __animation_end_handler(self, animated):
        joint = animated.name
        kx = animated.x
        ky = animated.y

        if self.joints_sprites is None or not joint in self.joints_sprites:
            return

        player_joint = self.joints_sprites[joint]
        px = player_joint.center_x
        py = player_joint.center_y

        dist = delta((kx, ky), (px, py))
        self.score.step(dist)

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
