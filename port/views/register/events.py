import arcade
import csv

from utils import chain
from path import Path
from pools import DataPool
from data import DATA_PATH


def save(self):
    path = Path(self.keypoints.pool, at=1)
    path.simplify()
    points = DataPool()
    points.pool = path.points
    with open(DATA_PATH / 'auto.csv', 'w') as moves:
        writer = csv.writer(moves, delimiter=',')
        points.each(lambda keypoint: writer.writerow(keypoint))


def to_menu(self):
    from views.menu import Menu
    self.pose.stop()
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, chain(save, to_menu)),
])
