import arcade
import csv

from utils import chain
from path import Path
from pools import DataPool
from data import DATA_PATH


def save(self):
    # path = Path(self.keypoints.pool, at=lambda el: el[1][0])
    # path.simplify()
    # points = DataPool()
    # points.pool = path.points
    # with open(DATA_PATH / 'auto.csv', 'w') as moves:
    #     writer = csv.writer(moves, delimiter=',')
    #     points.each(lambda keypoint: writer.writerow(keypoint))

    # print(self.keypoints)
    # for joint, pool in self.keypoints.items():
    #     print(pool.pool)

    paths = dict()
    combined = dict()
    for joint, pool in self.keypoints.items():
        paths[joint] = Path(pool.pool, at=1)
        paths[joint].simplify()

        for timestamp, point in paths[joint].points:
            if not timestamp in combined:
                combined[timestamp] = dict()
            combined[timestamp][joint] = point
    print(combined)
    with open(DATA_PATH / 'auto.csv', 'w') as moves:
        writer = csv.writer(moves, delimiter=',')
        rows = []
        for timestamp, joints in combined.items():
            row = [timestamp]
            for joint in self.joints_format:
                row += [joints[joint].x,
                        joints[joint].y] if joint in joints else [0, 0]
            print(row)
            rows.append(row)
        rows.sort(key=lambda row: row[0])
        writer.writerows(rows)


def to_menu(self):
    from views.menu import Menu
    self.pose.stop()
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, chain(save, to_menu)),
])
