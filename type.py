from typing import NamedTuple, TypedDict

PRIME = 2 ** 251 + 17 * 2 ** 192 + 1


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


def arr(self: ObjectState) -> list[str]:
    return [str(overflow(i)) for i in [self['pos'].x, self['pos'].y,
            self['vel'].x, self['vel'].y,
            self['acc'].x, self['acc'].y]]


def overflow(x):
    return (PRIME + x)if x < 0 else x


def is_nn(x: int) -> int: return 1 if x >= 0 else 0
