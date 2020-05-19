from utils import Point


class Pose:

    def __init__(self):
        self.off = 0
        self.stepLenght = 0.01
        self.A = 0
        self.B = 100
        self.X = 0
        self.Y = 100

    def pose(self):
        self.off += self.stepLenght
        return (Point(noise(self.off, self.A, self.X) * width, noise(self.off, self.A, self.Y) * height),
                Point(noise(self.off, self.B, self.X) * width, noise(self.off, self.B, self.Y) * height))
