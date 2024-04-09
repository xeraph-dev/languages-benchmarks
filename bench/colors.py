import re

RESET = "\x1b[0m"
BRIGHT = "\x1b[1m"
DIM = "\x1b[2m"
UNDERSCORE = "\x1b[4m"
REVERSE = "\x1b[7m"
HIDDEN = "\x1b[8m"
BLACK = "\x1b[30m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
WHITE = "\x1b[37m"
GRAY = "\x1b[90m"
BGBLACK = "\x1b[40m"
BGRED = "\x1b[41m"
BGGREEN = "\x1b[42m"
BGYELLOW = "\x1b[43m"
BGBLUE = "\x1b[44m"
BGMAGENTA = "\x1b[45m"
BGCYAN = "\x1b[46m"
BGWHITE = "\x1b[47m"
BGGRAY = "\x1b[100m"
RESET_PATTERN = re.compile(r"\x1b\[0m", re.IGNORECASE)


def reset(txt: str, COLOR: str | None = None) -> str:
    colors = RESET_PATTERN.findall(txt)
    strs = RESET_PATTERN.split(txt)
    merged = list[str]()
    prev = strs.pop(0)
    while prev is not None:
        merged.append(prev)
        if len(strs) == 0:
            break
        curr = strs.pop(0)
        if not curr:
            break
        merged.append(colors[0])
        if COLOR is not None:
            merged.append(COLOR)
        colors.pop(0)
        prev = curr
    merged.append(RESET)
    if COLOR is not None:
        merged.insert(0, COLOR)
    return "".join(merged)


def bright(txt: str) -> str:
    return reset(txt, BRIGHT)


def dim(txt: str) -> str:
    return reset(txt, DIM)


def underscore(txt: str) -> str:
    return reset(txt, UNDERSCORE)


def reverse(txt: str) -> str:
    return reset(txt, REVERSE)


def hidden(txt: str) -> str:
    return reset(txt, HIDDEN)


def black(txt: str) -> str:
    return reset(txt, BLACK)


def red(txt: str) -> str:
    return reset(txt, RED)


def green(txt: str) -> str:
    return reset(txt, GREEN)


def yellow(txt: str) -> str:
    return reset(txt, YELLOW)


def blue(txt: str) -> str:
    return reset(txt, BLUE)


def magenta(txt: str) -> str:
    return reset(txt, MAGENTA)


def cyan(txt: str) -> str:
    return reset(txt, CYAN)


def white(txt: str) -> str:
    return reset(txt, WHITE)


def gray(txt: str) -> str:
    return reset(txt, GRAY)


def bgblack(txt: str) -> str:
    return reset(txt, BGBLACK)


def bgred(txt: str) -> str:
    return reset(txt, BGRED)


def bggreen(txt: str) -> str:
    return reset(txt, BGGREEN)


def bgyellow(txt: str) -> str:
    return reset(txt, BGYELLOW)


def bgblue(txt: str) -> str:
    return reset(txt, BGBLUE)


def bgmagenta(txt: str) -> str:
    return reset(txt, BGMAGENTA)


def bgcyan(txt: str) -> str:
    return reset(txt, BGCYAN)


def bgwhite(txt: str) -> str:
    return reset(txt, BGWHITE)


def bggray(txt: str) -> str:
    return reset(txt, BGGRAY)
