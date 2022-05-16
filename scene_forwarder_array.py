from typing import Iterable
from type import *
from constant import *
from physics_engine import collision_pair_circles, friction_single_circle


def forward_scene_capped_counting_collision(arr_obj: list[ObjectState]) -> list[int]:
    return _recurse_euler_forward_scene_capped(arr_obj)


def _recurse_euler_forward_scene_capped(arr_obj) -> list[int]:
    arr_collision_record: list[int] = []
    for i in range(CP):
        arr_obj, arr_collision_record_next = _euler_forward_scene_one_step(
            arr_obj, i == 0)
        arr_collision_record.extend(arr_collision_record_next)
        # print(arr_collision_record_next)
        print(i, arr_obj)
        import sys
        sys.exit(0)
    return arr_collision_record


def _euler_forward_scene_one_step(arr_obj: list[ObjectState], first_step: bool):
    arr_obj_nxt, arr_collision_boundary, arr_collision_record = _recurse_euler_step_single_circle_aabb_boundary(
        arr_obj)
    print(arr_obj_nxt)
    collisions, dict_collision_count_init, arr_obj_after_col = _recurse_collision_handling_outer_loop(
        arr_obj, arr_obj_nxt)
    print(arr_obj_after_col)
    arr_collision_record.extend(collisions)
    arr_obj_after_friction = _recurse_handle_friction(arr_collision_boundary,
                                                      dict_collision_count_init, first_step, arr_obj_after_col)
    return arr_obj_after_friction, arr_collision_record


def _recurse_handle_friction(boundary_col:  list[int], balls_col: list[int], first_step: bool, arr_obj: list[ObjectState]):
    arr_obj_after_friction: list[ObjectState] = []
    for i, btw_col in enumerate(balls_col):
        has_collided = (first_step+btw_col+boundary_col[i])
        should_recal_friction = has_collided > 0
        obj_nxt = friction_single_circle(arr_obj[i], should_recal_friction)
        arr_obj_after_friction.append(obj_nxt)
    return arr_obj_after_friction


def _recurse_collision_handling_outer_loop(arr_obj: list[ObjectState], arr_obj_next: list[ObjectState]):
    n: int = len(arr_obj_next)
    dict_collision_count_init: list[int] = [0]*n
    arr_collision_record: list[int] = []
    for i in range(n):
        for j in range(i+1, n):
            obj_a_nxt, obj_b_nxt, bool_has_collided = collision_pair_circles(
                arr_obj[i], arr_obj[j], arr_obj_next[i], arr_obj_next[j])
            arr_obj_next[i] = obj_a_nxt
            arr_obj_next[j] = obj_b_nxt
            if bool_has_collided:
                dict_collision_count_init[i] += 1
                dict_collision_count_init[j] += 1
                # last * 4 + first * last + idx
                arr_collision_record.append(n * 4 + i * n + j)
    return arr_collision_record, dict_collision_count_init, arr_obj_next


def _recurse_euler_step_single_circle_aabb_boundary(arr_obj: Iterable[ObjectState]):
    arr_collision_record: list[int] = []
    arr_collision_boundary: list[int] = []
    arr_obj_nxt: list[ObjectState] = []
    for ind, obj in enumerate(arr_obj):
        obj_nxt, collision_with_boundary = euler_step_single_circle_aabb_boundary(
            obj)
        arr_obj_nxt.append(obj_nxt)
        arr_collision_boundary.append(int(collision_with_boundary))
        if collision_with_boundary:
            arr_collision_record.append(ind * 4 + int(collision_with_boundary))
    return arr_obj_nxt, arr_collision_boundary, arr_collision_record


def euler_step_single_circle_aabb_boundary(obj: ObjectState):
    # update pos
    x_nxt, vx_nxt, b_xmin, b_xmax = get_next_pos(obj, 0)
    y_nxt, vy_nxt, b_ymin, b_ymax = get_next_pos(obj, 1)
    collided_with_boundary = b_xmin + b_xmax*2 + b_ymin*3 + b_ymax*4
    return {
        "pos": Vec(x_nxt, y_nxt),
        "vel": Vec(vx_nxt, vy_nxt),
        "acc": obj['acc'],
    }, collided_with_boundary


def get_next_pos(obj: ObjectState, ind: int):
    x_min, x_max = (Params[ind*2+1]+Params[0], Params[ind*2+2]-Params[0])

    x_delta = mul_fp(obj['vel'][ind], dt)
    x_nxt_cand = x_delta + obj['pos'][ind]

    b_xmax = is_nn(x_nxt_cand - x_max)
    b_xmin = is_nn(x_min - x_nxt_cand)

    x_nxt = (1-b_xmax - b_xmin)*x_nxt_cand + b_xmax * x_max + b_xmin * x_min
    vx_nxt_cand = (1-b_xmax-b_xmin) * obj['vel'][ind] + \
        b_xmax * (-obj['vel'][ind]) + b_xmin * (-obj['vel'][ind])

    ax_dt = mul_fp(obj['acc'][ind], dt)
    ax_dt_abs = abs(ax_dt)
    vx_nxt_cand_abs = abs(vx_nxt_cand)
    bool_x_stopped = vx_nxt_cand_abs <= ax_dt_abs

    vx_nxt = 0 if bool_x_stopped else vx_nxt_cand + ax_dt
    return x_nxt, vx_nxt, b_xmin, b_xmax
