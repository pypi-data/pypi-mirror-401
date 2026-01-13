"""
Base64, but no UPPER CASE.

It is useful in case-insensitive scenarios, such as Scratch.
"""

import math

CHAR_MAP = "!#$%&()*,-.:;<>?@[]^_`{|}~abcdefghijklmnopqrstuvwxyz0123456789+/"


def encode(input: bytearray | bytes | str) -> str:
    if isinstance(input, str):
        input = input.encode()
    il = len(input)
    if il < 1:
        return ""
    out = [""] * (math.ceil(il / 3) * 4)
    ii: int = 0
    oi: int = 0
    cache: int = input[0]  # type: ignore

    def pp() -> int:
        nonlocal input, ii, il, cache
        r = cache
        ii += 1
        if ii < il:
            cache = input[ii]  # type: ignore
        else:
            cache = 0
        return r

    while ii < il:
        # 00000000 11111111 22222222
        # __000000 __001111 __111122 __222222
        out[oi] = CHAR_MAP[cache >> 2 & 63]
        oi += 1
        out[oi] = CHAR_MAP[(pp() << 4 | cache >> 4) & 63]
        oi += 1
        out[oi] = "=" if ii >= il else CHAR_MAP[(pp() << 2 | cache >> 6) & 63]
        oi += 1
        out[oi] = "=" if ii >= il else CHAR_MAP[pp() & 63]
        oi += 1
    return "".join(out)


def decode(input: str) -> bytearray:
    il = len(input)
    if il < 1:
        return bytearray(0)
    ol = math.floor(il / 4 * 3)
    if input[-1] == "=":
        ol -= 1 + (il > 1 and input[-2] == "=")
    out = bytearray(ol)
    ii: int = 0
    oi: int = 0
    character: str
    cache: int = 0

    def next() -> int:
        nonlocal input, ii, character, cache
        if ii >= il:
            cache = 0
            return 0
        character = input[ii]
        if character == "=":
            cache = 0
            return 0
        cache = CHAR_MAP.find(character)
        if cache < 0:
            raise ValueError(f"InvalidCharacterError: '{character}' at {ii}")
        ii += 1
        return cache

    while ii < il:
        # __000000 __111111 __222222 __333333
        # 00000011 11112222 22333333
        out[oi] = (next() << 2 | next() >> 4) & 255
        oi += 1
        if oi >= ol:
            break
        out[oi] = (cache << 4 | next() >> 2) & 255
        oi += 1
        if oi >= ol:
            break
        out[oi] = (cache << 6 | next()) & 255
        oi += 1
    return out


def decodeToStr(input: str, encoding: str = "utf-8", errors: str = "strict") -> str:
    return decode(input).decode(encoding, errors)
