from typing import TypeVar

T = TypeVar("T", int, float)


def clamp(v: T, lo: T, hi: T) -> T:
    if lo > hi:
        lo, hi = hi, lo
    return max(lo, min(v, hi))
