class Drawable:

    _fillv = (255, 255, 255)
    _strokev = (255, 255, 255, 0)

    def fill(self, *v):
        self._fillv = v
        return self

    def stroke(self, *v):
        self._strokev = v
        return self

    def onDraw(self):
        pass

    def draw(self):
        pushStyle()
        fill(*self._fillv)
        stroke(*self._strokev)
        self.onDraw()
        popStyle()


class Circle(Drawable):

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def onDraw(self):
        circle(self.x, self.y, self.r)


class Line(Drawable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def onDraw(self):
        line(self.a[0], self.a[1], self.b[0], self.b[1])


class Text(Drawable):

    def __init__(self, s, x, y):
        self.s = s
        self.x = x
        self.y = y

    def onDraw(self):
        textAlign(CENTER, CENTER)
        text(self.s, self.x, self.y)
