from views.song import Song
from views.register import Register


def to_song(view, *_):
    song = Song(view.width, view.height)
    song.setup()
    view.window.show_view(song)


def register(view, *_):
    register = Register(view.width, view.height)
    register.setup()
    view.window.show_view(register)
