# https://blog.logrocket.com/understanding-type-annotation-python/#what-mypy

from argparse import ArgumentParser, ArgumentTypeError
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
    elif id == 4:
        return {
            "score0":  Vec(200*FP,   62*FP),
            "score1":  Vec(62*FP,  200*FP),
            "forbid":  Vec(125*FP,   125*FP),
            "player":  Vec(20*FP,  20*FP),
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
    # record of collision
    arr_collision_record, list_of_records = forward_scene_capped_counting_collision(
        arr_obj)
    # fields
    score = _calculate_score_from_record(arr_collision_record)
    this_family = _serialize_collision_record_to_family(arr_collision_record)
    # test
    return list_of_records, score, this_family


def test(list_of_records, score, this_family, fileName):
    saved_records, saved_family, saved_score = get_records(fileName)
    check(saved_records, list_of_records)
    print(saved_records == list_of_records)
    print(saved_score == score)
    print(this_family == saved_family)


def check(a, b):
    for i, obj in enumerate(a):
        if obj != b[i]:
            print(i, obj, b[i])


def get_records(fileName):
    import json
    records: list[list[str]] = []
    with open(fileName, 'r') as f:
        obj = json.load(f)
        for event in obj['receipt']['events'][:-1]:
            records.append(event['data'][2:])
        last_event = obj['receipt']['events'][-1]['data']
        return records, int(last_event[5]), int(last_event[6])


def _serialize_collision_record_to_family(arr_collision_record: list[int]) -> int:
    sum: int = 0
    for i in arr_collision_record:
        sum = i + sum*28
    return sum % PRIME


def _calculate_score_from_record(arr_collision_record: list[int]):
    score_total: int = 0
    for i in arr_collision_record:
        score, is_reset = _parse_single_collision_record(i)
        if is_reset:
            score_total = 0
        else:
            score_total += score
    return score_total


def _parse_single_collision_record(record: int):
    if record == 19:
        return 10, 0
    elif record == 23:
        return 20, 0
    elif record == 27:
        return 0, 1
    else:
        return 0, 0


def run(level: int, x: int, y: int, run_test):
    list_of_records, score, this_family = submit_move_for_level(level, x, y)
    is_solution: bool = score != 0
    if run_test:
        test(list_of_records, score, this_family, run_test)
    print(
        f"is_solution: {is_solution} score: {score} this_family: {this_family}")


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def main():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', type=int, required=True)
    parser.add_argument('-x', type=int, required=True)
    parser.add_argument('-y', type=int, required=True)
    # parser.add_argument('-t', '--test', type=str2bool,
    #                     required=False, nargs='?')
    parser.add_argument('-t', '--test', type=str,
                        required=False, nargs='?')

    args = parser.parse_args()
    print(args.level, args.x, args.y)
    run(args.level, args.x, args.y, args.test)


if __name__ == '__main__':
    main()
else:
    pass
# print(submit_move_for_level(4, 2974341663658, -197967556159255)) b.json
# print(submit_move_for_level(3, 90000000000000, -125000000000000)) a.json
