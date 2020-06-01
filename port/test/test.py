import arcade


WIDTH = 800
HEIGHT = 600


class Menu(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu - click to advance", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK_LEATHER_JACKET, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game()
        game_view.setup()
        self.window.show_view(game_view)


class Game(arcade.View):
    def setup(self):
        pass

    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_RED)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game - press SPACE to advance", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK_LEATHER_JACKET, font_size=30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.SPACE:
            menu_view = Menu()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Menu + Game")
    menu_view = Menu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == '__main__':
    main()
