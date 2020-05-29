from processing import sound


def setup():
    size(1280, 720)
    background(0)

    global song
    song = sound.SoundFile(this, "audio/BVSC_HastaSiempre.mp3")

    song.play()


def draw():
    background(0)
    global song
    rect(0, 0, song.position() * width / song.duration(), height)


def mousePressed():
    global song
    if song.playing:
        song.pause()
    else:
        song.play()
