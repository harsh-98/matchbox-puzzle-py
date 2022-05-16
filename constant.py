# constant
# https://goerli.voyager.online/contract/0x00b28cf21b68b467414f014328aeccbad8c0dffb9618e086b09b3e584b77da47
FP: int = 1000000000000
CP: int = 40
dt: int = int(15*FP/100)
Params: list[int] = [20*FP, 0, 250*FP, 0, 250*FP]
FRICTION: int = 40*FP


def mul_fp(x: int, y: int) -> int:
    v = int((x*y)/FP)-1 if x*y < 0 and (x*y) % FP != 0 else int((x*y)/FP)
    return v


def div_fp(x: int, y: int) -> int:
    v = int((x*FP)/y)-1 if x*y < 0 and (x*FP) % y != 0 else int((x*FP)/y)
    return v
