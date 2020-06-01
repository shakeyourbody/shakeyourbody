import arcade
import csv

from utils import chain
from data import DATA_PATH


def save(self):
    with open(DATA_PATH / 'auto.csv', 'w') as moves:
        writer = csv.writer(moves, delimiter=',')
        self.keypoints.each(lambda keypoint: writer.writerow(keypoint))


def to_menu(self):
    from views.menu import Menu
    self.pose.stop()
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, chain(save, to_menu)),
])
