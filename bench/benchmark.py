import os
import subprocess
import time
from dataclasses import dataclass
from logging import Logger
from pathlib import Path

from bench.colors import yellow
from bench.config import Challenge, ChallengeDeveloper, ChallengeLevel, Config, Language
from bench.progress import Progress


@dataclass
class BenchmarkMeasure:
    time: int


@dataclass
class BenchmarkStats:
    challenge: str
    level: str
    language: str
    developer: str
    measures: list[BenchmarkMeasure]
    successes: int
    fails: int
    timeouts: int
    skips: int

    def __init__(
        self,
        challenge: Challenge,
        level: ChallengeLevel,
        language: Language,
        developer: ChallengeDeveloper,
    ) -> None:
        self.challenge = challenge.name
        self.level = level.name
        self.language = language.name
        self.developer = developer.username

        self.measures = []

        self.successes = 0
        self.fails = 0
        self.timeouts = 0
        self.skips = 0


def benchmark(
    logger: Logger, config: Config, challenges: list[Challenge]
) -> list[BenchmarkStats]:
    stats = list[BenchmarkStats]()

    total_progress = 0
    for challenge in challenges:
        for _ in challenge.levels:
            for developer in challenge.developers:
                for language in developer.languages:
                    total_progress += 1
    total_progress *= config.general.warmups + config.general.runs
    progress = Progress("Benchmarking", total_progress)

    logger.info("Benchmarking challenges")
    for challenge in challenges:
        for level in challenge.levels:
            for developer in challenge.developers:
                for language in developer.languages:
                    language = config.languages[language]

                    logger.info(
                        f"Benchmarking {yellow(language.name)} by developer {developer.username}, level {level.name} of challenge {challenge.key}"
                    )

                    stat = BenchmarkStats(challenge, level, language, developer)
                    stats.append(stat)

                    cwd = Path(os.getcwd()).joinpath(language.name)
                    cmd = language.cmd(challenge.key, developer.username)
                    if not cwd.joinpath(cmd).exists():
                        logger.warning(f"Missing file {cmd}, skipping")
                        stat.skips = config.general.runs
                        continue

                    cmd = [str(cmd)] + level.input

                    for i in range(config.general.warmups + config.general.runs):
                        progress.bar()

                        if (
                            i >= config.general.warmups
                            and stat.timeouts >= config.general.max_timeouts
                        ):
                            logger.warning(f"Reached max timeouts for {cmd}, skipping")
                            stat.skips = (
                                config.general.runs - config.general.warmups - i
                            )
                            break

                        try:
                            start = time.time_ns()
                            proc = subprocess.Popen(
                                cmd, cwd=cwd, stdout=subprocess.PIPE
                            )
                            proc.wait(config.general.timeout)
                            end = time.time_ns()

                            if i < config.general.warmups:
                                continue

                            output = None
                            if proc.stdout:
                                output = proc.stdout.read().strip().decode("utf-8")

                            delta = end - start
                            if proc.returncode != 0 or output != level.output:
                                stat.fails += 1
                                progress.error()
                            else:
                                stat.measures.append(BenchmarkMeasure(delta))
                                stat.successes += 1
                        except subprocess.TimeoutExpired:
                            if i < config.general.warmups:
                                continue
                            stat.timeouts += 1
                            progress.error()

                        progress.clear()

    return stats
