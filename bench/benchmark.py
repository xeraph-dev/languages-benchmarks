#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os
import subprocess
import time
from dataclasses import dataclass
from logging import Logger
from pathlib import Path

from .config import (
    Challenge,
    ChallengeDeveloper,
    ChallengeDeveloperName,
    ChallengeLanguage,
    ChallengeLanguageName,
    ChallengeLevel,
    ChallengeLevelName,
    ChallengeName,
    Config,
)
from .progress import Progress


@dataclass
class BenchmarkMeasure:
    time: int


@dataclass
class BenchmarkStats:
    challenge: ChallengeName
    level: ChallengeLevelName
    language: ChallengeLanguageName
    developer: ChallengeDeveloperName
    measures: list[BenchmarkMeasure]
    successes: int
    fails: int
    timeouts: int
    skips: int

    def __init__(
        self,
        challenge: Challenge,
        level: ChallengeLevel,
        language: ChallengeLanguage,
        developer: ChallengeDeveloper,
    ) -> None:
        self.challenge = challenge.key
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
    max_language_len = max(map(len, config.languages))
    stats = list[BenchmarkStats]()

    total_progress = 0
    for challenge in challenges:
        for _ in challenge.levels:
            for developer in challenge.developers:
                for _ in developer.languages:
                    total_progress += 1
    total_progress *= config.general.warmups + config.general.runs
    progress = Progress("Benchmarking", total_progress)

    for challenge in challenges:
        for level in challenge.levels:
            for developer in challenge.developers:
                for language_str in developer.languages:
                    language = config.languages[language_str]
                    challenge_language = ChallengeLanguage(
                        language.name.ljust(max_language_len)
                    )

                    logger.info(
                        f"Benchmarking {challenge} - {level} - {challenge_language} by {developer}"
                    )

                    stat = BenchmarkStats(
                        challenge,
                        level,
                        ChallengeLanguage(language.name),
                        developer,
                    )
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
