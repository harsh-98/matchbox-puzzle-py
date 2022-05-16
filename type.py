from typing import NamedTuple, TypedDict


class Vec(NamedTuple):
    x: int
    y: int


class LevelState(TypedDict):
    score0: Vec
    score1: Vec
    forbid: Vec
    player: Vec


class ObjectState(TypedDict):
    pos: Vec
    vel: Vec
    acc: Vec


def is_nn(x: int) -> int: return 1 if x >= 0 else 0
