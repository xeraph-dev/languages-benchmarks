#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os
import subprocess
from logging import Logger
from pathlib import Path

from .config import Challenge, Config
from .progress import Progress


def execute(cmd: list[str], cwd: Path) -> bool:
    try:
        subprocess.run(cmd, cwd=cwd, capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def build_challenges(
    logger: Logger, config: Config, challenges: list[Challenge]
) -> None:

    total_progress = sum(
        [
            1
            for challenge in challenges
            for developer in challenge.developers
            for language in developer.languages
            if not config.languages[language].simple_build
            and not config.languages[language].no_build
        ]
    )

    simple_build_languages = []
    [
        simple_build_languages.append(language)
        for challenge in challenges
        for language in challenge.languages
        if config.languages[language.name].simple_build
        and not config.languages[language.name].no_build
        and language not in simple_build_languages
    ]
    simple_build_languages.sort(key=lambda lang: lang.name)
    total_progress += len(simple_build_languages)

    progress = Progress("Building", total_progress)

    for language in simple_build_languages:
        challenges_included = []
        [
            challenges_included.append(f"{challenge.key}")
            for challenge in challenges
            if language in challenge.languages
        ]
        challenges_included.sort()

        developers_included = []
        [
            developers_included.append(f"{developer.username}")
            for challenge in challenges
            for developer in challenge.developers
            if language.name in developer.languages
            and f"{developer.username}" not in developers_included
        ]
        developers_included.sort()

        challenges_str = ", ".join(challenges_included)
        developers_str = ", ".join(developers_included)
        logger.info(
            f"Building [{challenges_str}] - {language.name} by [{developers_str}]"
        )
        with progress:
            cmd = config.languages[language.name].build_cmd("", "")
            cwd = Path(os.getcwd()).joinpath(language.name)
            if not execute(cmd, cwd):
                progress.clear()
                logger.error(
                    f"Build [{challenges_str}] - {language.name} by [{developers_str}] failed"
                )

    for challenge in challenges:
        languages = [
            language
            for language in challenge.languages
            if not config.languages[language.name].simple_build
            and not config.languages[language.name].no_build
        ]

        for language in languages:
            developers = [
                developer
                for developer in challenge.developers
                if language.name in developer.languages
            ]

            for developer in developers:
                logger.info(f"Building {challenge} - {language} by {developer}")
                with progress:
                    cmd = config.languages[language.name].build_cmd(
                        challenge.key, developer.username
                    )
                    cwd = Path(os.getcwd()).joinpath(language.name)
                    if not execute(cmd, cwd):
                        progress.clear()
                        logger.error(
                            f"Build {challenge} - {language} by {developer} failed"
                        )
