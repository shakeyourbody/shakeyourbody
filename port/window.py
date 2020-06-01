import arcade


class Window(arcade.Window):

    def __init__(self, WIDTH, HEIGHT, TITLE, fullscreen=True):
        super().__init__(WIDTH, HEIGHT, TITLE, fullscreen=fullscreen)
        self.adjust_viewport()

    def toggle_fullscreen(self):
        self.set_fullscreen(not self.fullscreen)
        self.adjust_viewport()

    def adjust_viewport(self):
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
