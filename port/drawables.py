import arcade


class Drawable:

    _fillv = (255, 255, 255)
    _strokev = (255, 255, 255, 0)

    def fill(self, *v):
        self._fillv = v
        return self

    def stroke(self, *v):
        self._strokev = v
        return self


class Circle(Drawable):

    def __init__(self, x, y, r, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.name = name

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.r, self._fillv)


class Line(Drawable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.stroke(255, 255, 255, 100)

    def draw(self):
        arcade.draw_line(self.a[0], self.a[1],
                         selfb[0], self.a[0], self._fillv)


class Text(Drawable):

    def __init__(self, s, x, y):
        self.s = s
        self.x = x
        self.y = y

    def draw(self):
        arcade.draw_text(self.s, self.x, self.y,
                         self._fillv, anchor_x="center")
