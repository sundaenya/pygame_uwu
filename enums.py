from enum import Enum


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class GameSettings(Enum):
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    WORLD_WIDTH = 4096
    WORLD_HEIGHT = 4096
    PLAYER_SIZE = 100
