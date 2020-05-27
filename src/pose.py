from functools import reduce
from operator import xor
from threading import Thread
import socket

from utils import Point, bits2float

# {0,  "Nose"},
# {1,  "Neck"},
# {2,  "RShoulder"},
# {3,  "RElbow"},
# {4,  "RWrist"},
# {5,  "LShoulder"},
# {6,  "LElbow"},
# {7,  "LWrist"},
# {8,  "MidHip"},
# {9,  "RHip"},
# {10, "RKnee"},
# {11, "RAnkle"},
# {12, "LHip"},
# {13, "LKnee"},
# {14, "LAnkle"},
# {15, "REye"},
# {16, "LEye"},
# {17, "REar"},
# {18, "LEar"},
# {19, "LBigToe"},
# {20, "LSmallToe"},
# {21, "LHeel"},
# {22, "RBigToe"},
# {23, "RSmallToe"},
# {24, "RHeel"},
# {25, "Background"}

pose_map = [
    "Nose",
    "Neck",
    "RShoulder",
    "RElbow",
    "RWrist",
    "LShoulder",
    "LElbow",
    "LWrist",
    "MidHip",
    "RHip",
    "RKnee",
    "RAnkle",
    "LHip",
    "LKnee",
    "LAnkle",
    "REye",
    "LEye",
    "REar",
    "LEar",
    "LBigToe",
    "LSmallToe",
    "LHeel",
    "RBigToe",
    "RSmallToe",
    "RHeel",
]


class Pose:

    IP = '127.0.0.1'
    PORT = 4124

    def __init__(self):

        self.connection = None
        self.running = False
        self._runner = None

        self._pose = None
        self._new = False

        self.MIRROR = False

    def connect(self):

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection.bind((Pose.IP, Pose.PORT))

        self.running = True
        self._runner = Thread(target=self.runner)
        self._runner.start()

        return self

    def runner(self):
        while self.running:

            buffer = [ord(b) for b in self.connection.recv(4096)]

            coords = [
                bits2float(reduce(xor, [
                    (buffer[j+k] & 0xFF) << (8*k) for k in [0, 1, 2, 3]
                ])) for j in map(lambda x: 4*x, range(len(pose_map)*2))
            ]

            coords_zipped = list(zip(coords[0::2], coords[1::2]))

            pose = dict()
            for i, key in enumerate(pose_map):
                x, y = coords_zipped[i]
                pose[key] = Point(x, y)

            self._pose = pose
            self._new = True

    def mirror(self, w=0):
        self.MIRROR = True
        self.W = w

    @property
    def pose(self):
        vpose = (self._pose, self._new)
        self._new = False
        return vpose

    def stop(self):
        self.running = False
        self._runner.join()
