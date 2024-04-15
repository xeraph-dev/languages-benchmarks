import os
from enum import Enum
from typing import Callable

from bench.colors import dim, green, red, yellow


class ProgressState(Enum):
    SUCCESS = 0
    ERROR = 1
    SKIP = 2

    def color(self) -> Callable[..., str]:
        match self.name:
            case "SUCCESS":
                return green
            case "SKIP":
                return yellow
            case "ERROR":
                return red


class Progress:
    name: str
    count: int
    total: int
    states: list[ProgressState]
    prev_bar: str

    def __init__(self, name: str, total: int) -> None:
        self.name = name
        self.count = 0
        self.total = total
        self.states = [ProgressState.SUCCESS for _ in range(total)]
        self.prev_bar = ""

    def error(self) -> None:
        self.states[self.count - 1] = ProgressState.ERROR

    def clear(self) -> None:
        print("\r\033[2K", end="")

    def bar(self, count: bool = False) -> None:
        self.clear()

        index = self.count if self.count == 0 else self.count - 1
        color = self.states[index].color()

        percentage = f"{yellow(f"{self.count * 100 // self.total}".rjust(3, " "))}%"
        state = f"{yellow(str(self.count))}/{yellow(str(self.total))}"

        columns, _ = os.get_terminal_size()
        columns -= 10 + len(self.name) + (len(str(self.total)) * 2)

        step_char = "■"
        step = step_char * (columns // self.total)
        incomplete = dim(step) * (self.total - self.count)
        step = color(step) if self.count > 0 else ""
        if self.total == self.count:
            step += color(step_char) * (columns % self.total)
        else:
            incomplete += dim(step_char) * (columns % self.total)
        bar_str = f"{self.prev_bar}{step}{incomplete}"
        self.prev_bar += step

        print(f"  {self.name} {state} {bar_str} {percentage}", end="\r")

        self.count += 0 if count else 1
