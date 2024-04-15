import os

from bench.colors import dim, green, red, yellow


class Progress:
    name: str
    count: int
    total: int
    errors: list[bool]
    prev_bar: str

    def __init__(self, name: str, total: int) -> None:
        self.name = name
        self.count = 0
        self.total = total
        self.errors = [False for _ in range(total)]
        self.prev_bar = ""

    def error(self) -> None:
        self.errors[self.count - 1] = True

    def clear(self) -> None:
        print("\r\033[2K", end="")

    def bar(self, count: bool = False) -> None:
        self.clear()

        color = red if self.errors[self.count - 1] else green

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
