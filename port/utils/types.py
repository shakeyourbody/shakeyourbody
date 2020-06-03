from dataclasses import dataclass
from collections import namedtuple


@dataclass
class Event:
    timestamp: float
    cbk: callable
    args: tuple

    def __call__(self):
        return self.cbk(*self.args)


Point = namedtuple(
    'Point',
    ['x', 'y']
)


filetypes = dict(
    audio=[
        ('audio', '*.mp3'),
        ('audio', '*.wav')
    ]
)
