from yaml import load, Loader
from pathlib import Path

BASE_PATH = Path(__file__).parent.absolute()

CONFIG_PATH = BASE_PATH / 'config.yaml'
with open(CONFIG_PATH, 'r') as stream:
    config = load(stream, Loader=Loader)

COLORS_PATH = BASE_PATH / 'colors.yaml'
with open(COLORS_PATH, 'r') as stream:
    colors = load(stream, Loader=Loader)

POSE_PATH = BASE_PATH / 'pose.yaml'
with open(POSE_PATH, 'r') as stream:
    pose = load(stream, Loader=Loader)
