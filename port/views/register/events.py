import arcade

from utils import chain


def save(self):
    print(self.keypoints.pool)


def to_menu(self, *_):
    from views.menu import Menu
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, chain(
        lambda view, *_: save(view),
        to_menu
    )),
])
