import arcade
from data import DATA_PATH


JOINTS_SPRITES = dict(
    Nose=arcade.Sprite(DATA_PATH/'graphic' /
                       'sprites'/'nose'/'nose.png', 0.04),
    RWrist=arcade.Sprite(DATA_PATH/'graphic'/'sprites' /
                         'hands'/'right.png', 0.04),
    LWrist=arcade.Sprite(DATA_PATH/'graphic'/'sprites' /
                         'hands'/'left.png', 0.04)
)
