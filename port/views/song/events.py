import arcade


def to_menu(self):
    from views.menu import Menu
    self.goto(Menu)


def to_score(self):
    from views.song import ScoreOut
    self.goto(ScoreOut, 0, self.score)


mapped = dict([
    (arcade.key.ESCAPE, to_menu),
])
