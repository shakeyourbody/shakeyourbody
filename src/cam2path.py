from pose import Pose
from utils import Point
from drawables import Text

import math

NPSTART = 20
NPEND = 10


POINTS = [
    Point(x=539.6967163085938, y=402.25665283203125),
    Point(x=429.7513732910156, y=411.7935485839844),
    Point(x=375.07086181640625, y=457.2342224121094),
    Point(x=319.9434814453125, y=475.95440673828125),
    Point(x=256.59423828125, y=494.0616149902344),
    Point(x=210.66319274902344, y=530.0526123046875),
    Point(x=411.4687805175781, y=457.3584289550781),
    Point(x=475.6016845703125, y=466.72271728515625),
    Point(x=539.7041015625, y=475.9148864746094),
    Point(x=676.352294921875, y=521.2512817382812)
]


def delta(p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)


def simplify(points, min):
    if len(points) <= min:
        return points

    imin = -1
    dmin = 999999999
    for i, _ in enumerate(points[1:-1]):
        db = delta(points[i-1], points[i])
        da = delta(points[i+1], points[i])
        d = da + db
        if d <= dmin:
            dmin = d
            imin = i

    if imin != -1:
        del points[imin]

    return simplify(points, min)


def setup():
    size(1280, 720)

    global points, opoints

    # Get the points from openpose
    p = Pose().connect()
    points = []
    while len(points) < NPSTART:
        coords, new = p.pose
        if new and 'nose' in coords:
            print '.',
            points.append(coords['nose'])
    p.stop()
    # points = POINTS

    # Old points to Text
    opoints = []
    for i, p in enumerate(points):
        opoints.append(Text(i, p.x, p.y))

    # Reduce the points
    points = simplify(points, NPEND)


def draw():
    background(0)

    global points, opoints

    for p in points:
        fill(255, 75)
        circle(p.x, p.y, 25)

    for point in opoints:
        point.fill(255, 0, 0).draw()
