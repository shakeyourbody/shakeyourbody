import arcade

from .events import mapped

from view import View
from config import colors
from data import DATA_PATH
from .events import goto_song, goto_register, goto_playground
colors = colors['menu']


class Button(arcade.gui.TextButton):

    def __init__(self, x, y, width, height, text, action, texture):

        theme = arcade.Theme()
        theme.set_font(24, arcade.color.WHITE_SMOKE)
        theme.add_button_textures(texture)

        super().__init__(x, y, width, height, text, theme=theme)
        self.action = action

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        self.action()


class Menu(View):

    def on_show(self):
        arcade.set_background_color(colors['bg'])

    def setup_buttons(self):
        width = 300
        height = 50
        delta = 55
        x = self.width / 2
        y = self.height / 3 + delta

        buttons = [
            ('PLAY', DATA_PATH / 'graphic' /
             'theme' / 'buttons' / 'button1.png', lambda: goto_song(self)),
            ('REGISTER', DATA_PATH / 'graphic' /
             'theme' / 'buttons' / 'button2.png', lambda: goto_register(self)),
            ('PLAY_GROUND', DATA_PATH / 'graphic' /
             'theme' / 'buttons' / 'button3.png', lambda: goto_playground(self))
        ]

        self.button_list = []
        for text, texture, action in buttons:
            self.button_list.append(
                Button(
                    x, y,
                    width, height,
                    text, action,
                    texture
                )
            )
            y -= delta

    def setup(self):
        self.setup_buttons()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text("Shake Yout Body!", self.width/2, self.height - self.height/3, colors['fg'],
                         font_size=50, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.setup_buttons()
