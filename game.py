# https://blog.logrocket.com/understanding-type-annotation-python/#what-mypy

from typing import NamedTuple, TypedDict
from constant import *
from type import *
from scene_forwarder_array import forward_scene_capped_counting_collision


def pull_level(id) -> LevelState:
    if id == 0:
        return {
            "score0": Vec(60*FP, 160*FP),
            "score1": Vec(210*FP, 160*FP),
            "forbid": Vec(125*FP, 160*FP),
            "player": Vec(40*FP, 40*FP),
        }
    elif id == 1:
        return {
            "score0": Vec(80*FP, 150*FP),
            "score1": Vec(180*FP, 175*FP),
            "forbid": Vec(80*FP, 200*FP),
            "player": Vec(175*FP, 40*FP),
        }
    elif id == 2:
        return {
            "score0": Vec(125*FP,   100*FP),
            "score1": Vec(125*FP,  50*FP),
            "forbid": Vec(125*FP, 150*FP),
            "player": Vec(125*FP,  230*FP),
        }
    elif id == 3:
        return {
            "score0": Vec(175*FP,   90*FP),
            "score1": Vec(90*FP,  125*FP),
            "forbid": Vec(50*FP,   175*FP),
            "player": Vec(200*FP,  40*FP),
        }
    return {
        "score0": Vec(80*FP, 150*FP),
        "score1": Vec(180*FP, 175*FP),
        "forbid": Vec(80*FP, 200*FP),
        "player": Vec(175*FP, 40*FP),
    }


def get_obj(pos: Vec, vel: Vec = Vec(0, 0)) -> ObjectState:
    return {
        "pos": pos,
        "vel": vel,
        "acc": Vec(0, 0),
    }


def submit_move_for_level(level: int, x: int, y: int):
    level_state = pull_level(level)
    arr_obj: list[ObjectState] = [
        get_obj(level_state['score0']),
        get_obj(level_state['score1']),
        get_obj(level_state['forbid']),
        get_obj(level_state['player'], Vec(x, y)),
    ]
    arr_collision_record = forward_scene_capped_counting_collision(
        arr_obj)
    score = _calculate_score_from_record(arr_collision_record)
    is_solution: bool = score != 0
    this_family = _serialize_collision_record_to_family(arr_collision_record)

    return is_solution, score, this_family


def _serialize_collision_record_to_family(arr_collision_record: list[int]) -> int:
    sum: int = 0
    for i in arr_collision_record:
        sum = i + sum*28
    return sum


def _calculate_score_from_record(arr_collision_record: list[int]):
    score_total: int = 0
    for i in arr_collision_record:
        score, is_reset = _parse_single_collision_record(i)
        if is_reset:
            score_total = 0
        else:
            score_total += score
    return score


def _parse_single_collision_record(record: int):
    if record == 19:
        return 10, 0
    elif record == 23:
        return 20, 0
    elif record == 27:
        return 0, 1
    else:
        return 0, 0


print(submit_move_for_level(3, 90000000000000, 125000000000000))
# print(submit_move_for_level(3, 125000000000000, 90000000000000))
