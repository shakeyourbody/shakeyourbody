import arcade

from .events import mapped, to_menu

from view import View
from data import DATA_PATH


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


class ScoreOut(View):

    def __init__(self, WIDTH, HEIGHT, score):
        super().__init__(WIDTH, HEIGHT)
        self.score = score

    def setup_buttons(self):
        self.button_list.append(
            Button(
                self.width/2, 100,
                300, 50,
                'MENU', lambda: to_menu(self),
                DATA_PATH / 'graphic' /
                'theme' / 'buttons' / 'button1.png'
            )
        )

    def setup(self):
        self.setup_buttons()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            f'Score: {self.score.score}',
            self.width/2, self.height/2,
            (245, 245, 245), font_size=50,
            anchor_x='center', anchor_y='center'
        )

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)

    def on_resize(self, w, h):
        super().on_resize(w, h)
        self.setup_buttons()
