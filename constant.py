# constant
# https://goerli.voyager.online/contract/0x00b28cf21b68b467414f014328aeccbad8c0dffb9618e086b09b3e584b77da47
FP: int = 1000000000000
CP: int = 40
dt: int = int(15*FP/100)
Params: list[int] = [20*FP, 0, 250*FP, 0, 250*FP]
FRICTION: int = 40*FP


def mul_fp(x: int, y: int) -> int: return int(x*y/FP)
def div_fp(x: int, y: int) -> int: return int((x*FP)/y)
