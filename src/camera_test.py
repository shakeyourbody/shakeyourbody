from timedEvent import Frame
from processing import video
from gab import opencv

cam = Frame(None)
cv = Frame(None)


def setup():
    # size(640, 480)
    size(1280, 480)

    cam.set(video.Capture(this, video.Capture.list()[0]))
    cam.v.start()

    cv.set(opencv.OpenCV(this, 640, 480))


def draw():
    background(255, 255, 255, 100)

    if cam.v.available():
        cam.v.read()

    image(cam.v, 0, 0)

    cv.v.loadImage(cam.v)
    cv.v.calculateOpticalFlow()

    translate(cam.v.width, 0)
    stroke(0, 0, 0, 100)
    cv.v.drawOpticalFlow()
