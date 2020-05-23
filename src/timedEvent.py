from threading import Thread
from time import time
from collections import namedtuple
from utils import run_safe


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
                run_safe(self.CBK(*self.ARGS))
                self.running = False


def delayed(timestamp):
    def wrapper(cbk):
        def caller(*args):
            Event(timestamp, cbk, *args).start()
        return caller
    return wrapper


class Pool:

    def __init__(self):
        self.EVENTS = []

        self.running = False
        self._runner = None

        self.NOTIFICATIONS = dict()

    def at(self, timestamp, cbk, *args):
        self.EVENTS.append((timestamp, cbk, args))

    def start(self):
        self.EVENTS.sort(key=lambda e: e[0], reverse=False)
        self._runner = Thread(target=self.runner)
        self._runner.start()

    def stop(self):
        self.running = False
        try:                        # TODO: refactor, dirty
            self._runner.join()     # should be avoided with some if, but
        except AttributeError:      # for now it will be ok
            pass

    def clear(self):
        self.EVENTS = []

    def runner(self):
        self.running = True
        index = 0
        self.TINIT = time()
        self._notify('start')
        while len(self.EVENTS) > index and self.running:
            elapsed = time() - self.TINIT
            if elapsed >= self.EVENTS[index][0]:
                self.EVENTS[index][1](*self.EVENTS[index][2])
                index += 1
        self._notify('end')
        self._notify('end:ok' if self.running else 'end:notOk')
        self.TINIT = -1
        self.running = False
        self._runner = None

    def on(self, n, cbk):
        self.NOTIFICATIONS[n] = cbk

    def _notify(self, n):
        if n in self.NOTIFICATIONS and self.NOTIFICATIONS[n]:
            run_safe(self.NOTIFICATIONS[n])


class Frame:

    @staticmethod
    def cbk(v):
        return lambda f: f.set(v)

    def __init__(self, v=None):
        self.v = v

    def set(self, v):
        self.v = v


def animate(length):
    then = Frame()
    end = Frame()
    animation = Frame()
    loop_if = Frame()

    caller = namedtuple(
        'Caller', ['animation', 'then', 'end', 'loop_if'])

    def wrapper(setter):
        def animator(self=None, *args, **kwargs):
            setter(self, caller(animation.set, then.set, end.set,
                                loop_if.set), *args, **kwargs)
            start = time()
            elapsed = 0
            while run_safe(loop_if.v) and elapsed < length:
                run_safe(animation.v, elapsed)
                elapsed = time() - start
            diff = elapsed - length == 0
            run_safe(then.v if diff else None)
            run_safe(end.v, diff)
        return animator

    return wrapper
