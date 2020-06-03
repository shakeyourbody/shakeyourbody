import arcade

from views.song import Song
from views.register import Register
from views.playground import Playground
from utils.dialogs import openfile
from utils.types import filetypes


def goto_register(self):
    song_path = openfile(title='Select a song', filetypes=filetypes['audio'])
    self.goto(Register, 3, song_path)


mapped = dict([
    (arcade.key.ESCAPE, lambda *_: arcade.close_window()),
    (arcade.key.F, lambda view, *_: view.window.toggle_fullscreen()),
    (arcade.key.ENTER, lambda view, *_: view.goto(Song, 3)),
    (arcade.key.R, goto_register),
    (arcade.key.P, lambda view, *_: view.goto(Playground))
])
