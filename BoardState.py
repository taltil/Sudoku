from enum import Enum


class BoardState(Enum):
    NOT_FULL = -1
    FULL_AND_WRONG = 1
    FULL_AND_RIGHT = 2
