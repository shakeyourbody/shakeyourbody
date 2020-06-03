import arcade
from threading import Thread


class View(arcade.View):

    def __init__(self, WIDTH, HEIGHT):
        super().__init__()

        self.width = WIDTH
        self.height = HEIGHT

        self.LOADED = True

    def on_resize(self, width, height):
        self.width = width
        self.height = height

    def setup(self):
        pass

    def goto(self, Target):
        target = Target(self.width, self.height)
        target_setupper = Thread(target=target.setup)
        target_setupper.start()
        loader = Loader(self.width, self.height, target, target_setupper)
        self.window.show_view(loader)


class Loader(View):

    def __init__(self, WIDTH, HEIGHT, target, setupper):
        super().__init__(WIDTH, HEIGHT)
        self.dots = ''
        self.clock = 0
        self.target = target
        self.setupper = setupper

    def on_show(self):
        arcade.set_background_color((35, 43, 43))

    def on_update(self, elapsed):
        self.clock += elapsed
        self.dots = '.' * int((self.clock % 1) * 4)

        if self.target.LOADED:
            self.setupper.join()
            self.window.show_view(self.target)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"loading{self.dots}", self.width/2, self.height/2, (245, 245, 245),
                         font_size=10, anchor_x="center", anchor_y="center")
