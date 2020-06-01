import arcade


class View(arcade.View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__()

        self.width = WIDTH
        self.height = HEIGHT

    def on_resize(self, width, height):
        self.width = width
        self.height = height

    def setup(self):
        pass

    def goto(self, Target):
        target = Target(self.width, self.height)
        target.setup()
        self.window.show_view(target)
