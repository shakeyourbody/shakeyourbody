from .openpose import Pose

from data.graphic.sprites import JOINTS_SPRITES
from drawables import Circle, Text
from pools import DataPool


class Pose(Pose):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__(WIDTH, HEIGHT)
        self.sprites = JOINTS_SPRITES
        self.unsprited_joints = DataPool()

    def joints(self):
        coords, new = self.pose
        if coords is None:
            return None, None
        if not new:
            return self.sprites, self.unsprited_joints

        self.unsprited_joints.clear()
        for joint in coords:
            x, y = coords[joint]
            if x != 0 and y != 0:
                x = self.WIDTH - self.WIDTH * x
                y = self.HEIGHT - self.HEIGHT * y * 2
                if joint in self.sprites:
                    self.sprites[joint].center_x = x
                    self.sprites[joint].center_y = y
                else:
                    self.unsprited_joints.append(
                        Circle(x, y, 10).fill(245, 245, 245, 10))
                    self.unsprited_joints.append(
                        Text(joint, x, y).fill(220, 220, 220))

        return self.sprites, self.unsprited_joints
