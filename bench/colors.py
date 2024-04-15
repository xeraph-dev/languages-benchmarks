import re

RESET = "\x1b[000m"
BRIGHT = "\x1b[001m"
DIM = "\x1b[002m"
UNDERSCORE = "\x1b[004m"
REVERSE = "\x1b[007m"
HIDDEN = "\x1b[008m"
BLACK = "\x1b[030m"
RED = "\x1b[031m"
GREEN = "\x1b[032m"
YELLOW = "\x1b[033m"
BLUE = "\x1b[034m"
MAGENTA = "\x1b[035m"
CYAN = "\x1b[036m"
WHITE = "\x1b[037m"
GRAY = "\x1b[090m"
BGBLACK = "\x1b[040m"
BGRED = "\x1b[041m"
BGGREEN = "\x1b[042m"
BGYELLOW = "\x1b[043m"
BGBLUE = "\x1b[044m"
BGMAGENTA = "\x1b[045m"
BGCYAN = "\x1b[046m"
BGWHITE = "\x1b[047m"
BGGRAY = "\x1b[100m"
RESET_PATTERN = re.compile(r"\x1b\[000m", re.IGNORECASE)


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
