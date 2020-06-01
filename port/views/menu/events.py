import arcade

from .actions import to_song, register
from views.song import Song
from views.register import Register

mapped = dict([
    (arcade.key.ESCAPE, lambda *_: arcade.close_window()),
    (arcade.key.F, lambda view, *_: view.window.toggle_fullscreen()),
    (arcade.key.ENTER, lambda view, *_: view.goto(Song)),
    (arcade.key.R, lambda view, *_: view.goto(Register))
])
