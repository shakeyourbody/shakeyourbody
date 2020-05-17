from threading import Thread
from time import time
import csv
import threading


class TimedStream:

    def __init__(self, pool):
        self.EVENTS = []
        self.TINIT = -1
        self.POOL = pool

        self._runnerT = None

    def at(self, timestap, value):
        self.EVENTS.append((timestap, value))
        return self

    def start(self):
        self.EVENTS.sort(key=lambda e: e[0], reverse=False)
        self._runnerT = Thread(target=self.runner)
        self._runnerT.start()
        return self

    def stop(self):
        if self._runnerT is not None:
            self._runnerT.join()

    def runner(self):
        self.TINIT = time()
        while len(self) > 0:
            elapsed = time() - self.TINIT
            if abs(self.EVENTS[0][0] - elapsed) < 0.1:
                self.POOL = self.EVENTS[0][1]
                print(self.EVENTS[0][0], self.POOL)
                self.EVENTS = self.EVENTS[1:]
        self.TINIT = -1
        self.runnerT = None

    def __len__(self):
        return len(self.EVENTS)

    def __call__(self):
        return self.POOL
