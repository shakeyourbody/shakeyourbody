from threading import Thread
from time import time


class Event:

    def __init__(self, timestamp, cbk, *args):
        self.TIMESTAMP = timestamp
        self.CBK = cbk
        self.ARGS = args

        self.running = False
        self._runner = None

    def start(self):
        self._runner = Thread(target=self.runner)
        self.running = True
        self._runner.start()

    def runner(self):
        start = time()
        while self.running:
            elapsed = time() - start
            if self.TIMESTAMP is not None and elapsed >= self.TIMESTAMP:
                if self.CBK is not None:
                    self.CBK(*self.ARGS)
                self.running = False


class Pool:

    def __init__(self):
        self.EVENTS = []

        self.running = False
        self._runner = None

    def at(self, timestamp, cbk, *args):
        self.EVENTS.append((timestamp, cbk, args))
        return self

    def start(self):
        self.EVENTS.sort(key=lambda e: e[0], reverse=False)
        self._runner = Thread(target=self.runner)
        self._runner.start()

    def stop(self):
        self.running = False
        if self._runner is not None:
            self._runner.join()

    def runner(self):
        self.running = True
        self.TINIT = time()
        index = 0
        while len(self.EVENTS) > index and self.running:
            elapsed = time() - self.TINIT
            if elapsed >= self.EVENTS[index][0]:
                self.EVENTS[index][1](*self.EVENTS[index][2])
                print(self.EVENTS[index][0])
                index += 1
        self.TINIT = -1
        self.running = False
        self._runner = None


class Frame:

    @staticmethod
    def cbk(v):
        return lambda f: f.set(v)

    def __init__(self, v=None):
        self.v = v

    def set(self, v):
        self.v = v
