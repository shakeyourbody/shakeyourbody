from utils.types import Point
from random import random


class Pose:

    def __init__(self):
        self._pose = None

    @property
    def pose(self):
        return (dict(
            Nose=Point(random(), random())
        ), True)

    def stop(self):
        pass
