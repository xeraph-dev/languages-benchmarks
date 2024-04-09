from logging import Logger

from bench.config import Challenge


class Builder:
    logger: Logger
    challenges: list[Challenge]

    def __init__(self, logger: Logger, challenges: list[Challenge]) -> None:
        self.logger = logger
        self.challenges = challenges

    def build(self) -> None:
        self.logger.info("Building challenges")
        pass
