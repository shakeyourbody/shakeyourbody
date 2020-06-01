import arcade

from .events import mapped

from view import View
from config import colors
colors = colors['menu']


class Menu(View):

    def on_show(self):
        arcade.set_background_color(colors['bg'])

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu", self.width/2, self.height/2, colors['fg'],
                         font_size=30, anchor_x="center", anchor_y="center")

    def on_key_press(self, key, modifiers):
        if key in mapped:
            mapped[key](self)
