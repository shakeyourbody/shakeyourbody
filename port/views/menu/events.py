import arcade

from views.song import Song
from views.register import Register
from views.playground import Playground


mapped = dict([
    (arcade.key.ESCAPE, lambda *_: arcade.close_window()),
    (arcade.key.F, lambda view, *_: view.window.toggle_fullscreen()),
    (arcade.key.ENTER, lambda view, *_: view.goto(Song, 3)),
    (arcade.key.R, lambda view, *_: view.goto(Register, 0)),
    (arcade.key.P, lambda view, *_: view.goto(Playground))
])
