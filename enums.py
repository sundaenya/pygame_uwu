from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class GameSettings(Enum):
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    WORLD_WIDTH = 2000
    WORLD_HEIGHT = 2000
    PLAYER_SIZE = 100
