import arcade

from views.menu import Menu
from window import Window
from config import config
from pose.openpose import RUNNING_POSES

WIDTH = config['window']['width']
HEIGHT = config['window']['height']
TITLE = config['window']['title']
FULLSCREEN = config['window']['fullscreen']


def main():
    window = Window(WIDTH, HEIGHT, TITLE, fullscreen=FULLSCREEN)
    menu = Menu(WIDTH, HEIGHT)
    menu.setup()
    window.show_view(menu)
    arcade.run()

    RUNNING_POSES.each(lambda pose: pose.stop())


if __name__ == "__main__":
    main()
