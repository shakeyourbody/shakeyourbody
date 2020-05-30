from functools import reduce
from operator import xor
from threading import Thread
import socket

from utils import Point, bits2float


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

            buffer = [ord(b) for b in self.connection.recv(1024)]

            nosex, nosey, rwristx, rwristy, lwristx, lwristy = [
                bits2float(reduce(xor, [
                    (buffer[j+k] & 0xFF) << (8*k) for k in [0, 1, 2, 3]
                ])) for j in [0, 4, 8, 12, 16, 20]
            ]

            self._pose = {
                'nose': Point(self.W - nosex if self.MIRROR else nosex, nosey),
                'rwrist': Point(self.W - rwristx if self.MIRROR else rwristx, rwristy),
                'lwrist': Point(self.W - lwristx if self.MIRROR else lwristx, lwristy)
            }
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
