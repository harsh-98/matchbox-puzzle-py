from type import *
from constant import *
import math


def collision_pair_circles(c1: ObjectState, c2: ObjectState,  c1_cand: ObjectState, c2_cand: ObjectState):
    circle_r = Params[0]
    circle_r2_sq = (circle_r*2)**2/FP
    x1mx2 = c1_cand['pos'].x - c2_cand['pos'].x
    x1mx2_sq = mul_fp(x1mx2, x1mx2)

    y1mx2 = c1_cand['pos'].y - c2_cand['pos'].y
    y1my2_sq = mul_fp(y1mx2, y1mx2)

    d12_sq = x1mx2_sq + y1my2_sq

    bool_c1_c2_cand_collided = d12_sq <= circle_r2_sq
    # not collided
    x1_nxt = c1_cand['pos'].x
    y1_nxt = c1_cand['pos'].y
    x2_nxt = c2_cand['pos'].x
    y2_nxt = c2_cand['pos'].y
    vx1_nxt = c1_cand['vel'].x
    vy1_nxt = c1_cand['vel'].y
    vx2_nxt = c2_cand['vel'].x
    vy2_nxt = c2_cand['vel'].y
    # collided
    if bool_c1_c2_cand_collided:
        d_cand = distance_2pt(c1_cand['pos'], c2_cand['pos'])
        nom = 2*circle_r - d_cand
        d = distance_2pt(c1['pos'], c2['pos'])
        denom = d - d_cand

        def cor_next(a, b): return b - div_fp(mul_fp(nom, b-a), denom)

        x1_nxt = cor_next(c1['pos'].x, c1_cand['pos'].x)
        y1_nxt = cor_next(c1['pos'].y, c1_cand['pos'].y)

        x2_nxt = cor_next(c2['pos'].x, c2_cand['pos'].x)
        y2_nxt = cor_next(c2['pos'].y, c2_cand['pos'].y)

        alpha_nom1 = mul_fp(c2['vel'].x - c1['vel'].x, x2_nxt - x1_nxt)
        alpha_nom2 = mul_fp(c2['vel'].y - c1['vel'].y, y2_nxt - y1_nxt)

        alpha_denom1 = mul_fp(x2_nxt - x1_nxt, x2_nxt - x1_nxt)
        alpha_denom2 = mul_fp(y2_nxt - y1_nxt, y2_nxt - y1_nxt)

        alpha = div_fp(alpha_nom1+alpha_nom2, alpha_denom1+alpha_denom2)

        def vel_next(v, diff): return v - mul_fp(alpha, diff)

        vx1_nxt = vel_next(c1['vel'].x, x1_nxt - x2_nxt)
        vy1_nxt = vel_next(c1['vel'].y, y1_nxt - y2_nxt)

        vx2_nxt = vel_next(c2['vel'].x, x2_nxt - x1_nxt)
        vy2_nxt = vel_next(c2['vel'].y, y2_nxt - y1_nxt)

    c1_nxt = {
        "pos": Vec(x1_nxt, y1_nxt),
        "vel": Vec(vx1_nxt, vy1_nxt),
        "acc": c1["acc"],
    }
    c2_nxt = {
        "pos": Vec(x2_nxt, y2_nxt),
        "vel": Vec(vx2_nxt, vy2_nxt),
        "acc": c2["acc"],
    }
    return c1_nxt, c2_nxt, bool_c1_c2_cand_collided


def distance_2pt(pt2: Vec, pt1: Vec) -> int:
    distance_2 = (pt2.x-pt1.x) * (pt2.x-pt1.x) + (pt2.y-pt1.y) * (pt2.y-pt1.y)
    return int(math.sqrt(distance_2))


def friction_single_circle(obj: ObjectState, should_recal_friction: bool):
    ax_nxt, ay_nxt = 0, 0
    if should_recal_friction:
        v = distance_2pt(obj['vel'], Vec(0, 0))
        if v != 0:
            a_mul_vx = mul_fp(FRICTION, -1*obj['vel'].x)
            ax_nxt = div_fp(a_mul_vx, v)
            a_mul_vy = mul_fp(FRICTION,  - 1*obj['vel'].y)
            ay_nxt = div_fp(a_mul_vy, v)
    else:
        if obj['vel'].x == 0:
            ax_nxt = 0
        else:
            ax_nxt = obj['acc'].x

        if obj['vel'].y == 0:
            ay_nxt = 0
        else:
            ay_nxt = obj['acc'].y
    return {
        "pos": obj["pos"],
        "vel": obj["vel"],
        "acc": Vec(ax_nxt, ay_nxt),
    }
