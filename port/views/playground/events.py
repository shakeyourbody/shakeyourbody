import arcade


def to_menu(self, *_):
    from views.menu import Menu
    self.pose.stop()
    self.goto(Menu)


mapped = dict([
    (arcade.key.ESCAPE, to_menu),
])
