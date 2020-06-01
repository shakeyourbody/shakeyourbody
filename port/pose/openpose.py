from functools import reduce
from operator import xor
from threading import Thread
import socket

from utils.types import Point
from utils import bits2float
from config import pose as config
from pools import DataPool

IP = config['ip']
PORT = config['port']
JOINTS = config['joints']


RUNNING_POSES = DataPool()


def parse_buffer_manually(buffer, joints, width, height):

    coords = [
        bits2float(reduce(xor, [
            (buffer[j+k] & 0xFF) << (8*k) for k in [0, 1, 2, 3]
        ])) for j in map(lambda x: 4*x, range(len(joints)*2))
    ]

    coords_zipped = list(zip(coords[0::2], coords[1::2]))

    pose = dict()
    for i, key in enumerate(joints):
        x, y = coords_zipped[i]
        pose[key] = Point(x/width, y/width)

    return pose


def parse_buffer_struct(buffer, joints):

    # TODO: use ctypes and struct to parse the incoming buffer
    # REFERENCE: https://stackoverflow.com/questions/48822543/reading-a-c-struct-via-sockets-into-python

    pass


class Pose:

    def __init__(self, WIDTH, HEIGHT, POSE_SET=JOINTS['source']):

        self.connection = None
        self.running = False
        self.__runner = None

        self.__pose = None
        self.__new = None

        self.__joints = JOINTS[POSE_SET]

        # TODO: normalize joints position in openpose client code
        self.WDITH = WIDTH
        self.HEIGHT = HEIGHT

        RUNNING_POSES.append(self)

    def connect(self):
        self.running = True
        self.__runner = Thread(target=self.runner)
        self.__runner.start()

    def wait(self):
        while self.pose[0] is None:
            pass

    def runner(self):

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection.bind((IP, PORT))
        self.connection.settimeout(1)

        while self.running:

            try:
                buffer = self.connection.recv(4096)
                self.__new = True
                self.__pose = parse_buffer_manually(
                    buffer,
                    self.__joints,
                    self.WDITH,
                    self.HEIGHT
                )
            except socket.timeout:
                pass

        self.connection.close()

    @property
    def pose(self):
        vpose = (self.__pose, self.__new)
        self.__new = False
        return vpose

    def stop(self):
        self.running = False
        self.__runner.join()
        RUNNING_POSES.remove(self)
