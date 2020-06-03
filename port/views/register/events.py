import arcade
import csv
import os

from utils import chain
from path import Path
from pools import DataPool
from data import DATA_PATH


def save(self):
    paths = dict()
    combined = dict()
    for joint, pool in self.keypoints.items():
        paths[joint] = Path(pool.pool, at=1)
        paths[joint].simplify()

        for timestamp, point in paths[joint].points:
            if not timestamp in combined:
                combined[timestamp] = dict()
            combined[timestamp][joint] = point

    folder = DATA_PATH / 'registered'
    if not os.path.isdir(str(folder)):
        os.mkdir(str(folder))

    with open(folder / 'moves.csv', 'w') as moves:
        writer = csv.writer(moves, delimiter=',')
        rows = []
        for timestamp, joints in combined.items():
            row = [timestamp]
            for joint in self.joints_format:
                row += [joints[joint].x,
                        joints[joint].y] if joint in joints else [0, 0]
            all_zeros = True
            for coord in row[1:]:
                if not coord == 0:
                    all_zeros = False
            if not all_zeros:
                rows.append(row)
        rows.sort(key=lambda row: row[0])
        writer.writerows(rows)

    with open(folder / 'song.path', 'w') as song:
        song.write(self.song_path)


def to_menu(self):
    from views.menu import Menu
    self.pose.stop()
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, chain(save, to_menu)),
])
