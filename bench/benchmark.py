import resource
import subprocess
import time
from dataclasses import dataclass
from logging import Logger
from typing import List

from bench.config import Challenge, Config, Language, Level


@dataclass
class BenchmarkStat:
    challenge: str
    level: str
    language: str
    time: List[int]
    ram: List[int]
    success: int
    fail: int
    timeout: int

    def __init__(self, challenge: Challenge, level: Level, language: Language) -> None:
        self.challenge = challenge.key
        self.level = level.name
        self.language = language.name

        self.time = []
        self.ram = []

        self.success = 0
        self.fail = 0
        self.timeout = 0


class Benchmark:
    logger: Logger
    config: Config
    challenges: List[Challenge]
    stats = list[BenchmarkStat]()

    def __init__(
        self, logger: Logger, config: Config, challenges: List[Challenge]
    ) -> None:
        self.logger = logger
        self.challenges = challenges
        self.config = config

    def run(self) -> None:
        for challenge in self.challenges:
            for level in challenge.levels:
                for language in level.languages:
                    stat = BenchmarkStat(challenge, level, language)
                    self.stats.append(stat)

                    bin_path = language.bin(challenge.key)
                    cmd = [bin_path] + level.input

                    if not bin_path.exists():
                        self.logger.info("building", challenge.key, language.name)
                        continue

                    for i in range(self.config.warmups + self.config.runs):
                        try:
                            start = time.time_ns()

                            proc = subprocess.Popen(
                                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                            )
                            proc.wait(self.config.timeout)

                            end = time.time_ns() - start
                            rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
                            if proc.stdout:
                                output = proc.stdout.read().strip().decode("utf-8")

                            if i < self.config.warmups:
                                continue
                            if proc.returncode == 0 and output == level.output:
                                stat.success += 1
                                stat.time.append(end)
                                stat.ram.append(rss)
                            else:
                                stat.fail += 1
                        except subprocess.TimeoutExpired:
                            if i < self.config.warmups:
                                continue
                            stat.timeout += 1

    def print(self) -> None:
        print(self.stats)
