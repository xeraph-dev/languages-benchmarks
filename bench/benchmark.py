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


def compute(
    logger: Logger,
    config: Config,
    progress: Progress,
    stats: list[BenchmarkStats],
    challenge: Challenge,
    level: ChallengeLevel,
    language: ChallengeLanguage,
    developer: ChallengeDeveloper,
):
    if language.name not in developer.languages:
        return

    logger.info(f"Benchmarking {challenge} - {level} - {language} by {developer}")

    stat = BenchmarkStats(
        challenge,
        level,
        ChallengeLanguage(language.name),
        developer,
    )
    stats.append(stat)

    cwd = Path(os.getcwd()).joinpath(language.name)
    cmd = config.languages[language.name].cmd(challenge.key, developer.username)
    no_build = config.languages[language.name].no_build
    executable = cmd[1] if no_build else cmd[0]

    if not cwd.joinpath(executable).exists():
        logger.warning(f"Missing file {executable}, skipping")
        stat.skips = config.general.runs
        return

    cmd = cmd + level.input

    for i in range(config.general.warmups + config.general.runs):
        with progress:
            if (
                i >= config.general.warmups
                and stat.timeouts >= config.general.max_timeouts
            ):
                logger.warning(f"Reached max timeouts for {cmd}, skipping")
                stat.skips = config.general.runs - config.general.warmups - i
                break
            try:
                start = time.time_ns()
                proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE)
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
            except OSError as e:
                if i < config.general.warmups:
                    continue
                stat.fails += 1
                progress.error()


def benchmark(
    logger: Logger, config: Config, challenges: list[Challenge]
) -> list[BenchmarkStats]:
    stats = list[BenchmarkStats]()

    total_progress = sum(
        [
            1
            for challenge in challenges
            for _ in challenge.levels
            for developer in challenge.developers
            for _ in developer.languages
        ]
    ) * (config.general.warmups + config.general.runs)

    progress = Progress("Benchmarking", total_progress)

    [
        compute(logger, config, progress, stats, challenge, level, language, developer)
        for challenge in challenges
        for level in challenge.levels
        for language in challenge.languages
        for developer in challenge.developers
    ]

    return stats
