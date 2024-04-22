#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os
import subprocess
from logging import Logger
from pathlib import Path

from .colors import green, yellow
from .config import Challenge, ChallengeLanguage, Config
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
    max_language_len = max(map(len, config.languages))

    total_progress = 0
    for challenge in challenges:
        languages_added = set[str]()
        for developer in challenge.developers:
            for language in developer.languages:
                language = config.languages[language]
                if language.simple_build and language.name not in languages_added:
                    total_progress += 1
                elif not language.simple_build:
                    total_progress += 1

                languages_added.add(language.name)
    progress = Progress("Building", total_progress)

    for challenge in challenges:
        languages = set[str]()
        languages_built = set[str]()
        for developer in challenge.developers:
            developer_languages_built = set[str]()
            for language in developer.languages:
                language = config.languages[language]
                challenge_language = ChallengeLanguage(
                    language.name.ljust(max_language_len)
                )
                cwd = Path(os.getcwd()).joinpath(language.name)

                if language.simple_build and language.name not in languages_built:
                    logger.info(f"Building {challenge} - {challenge_language}")
                    cmd = language.build_cmd(challenge.key, "")
                    progress.bar()
                    if execute(cmd, cwd):
                        developer_languages_built.add(language.name)
                    else:
                        progress.clear()
                        logger.error(
                            f"Failed building {yellow(language.name)} for challenge {green(challenge.key)}"
                        )
                        progress.error()
                elif not language.simple_build:
                    logger.info(
                        f"Building {challenge} - {challenge_language} by {developer}"
                    )
                    cmd = language.build_cmd(challenge.key, developer.username)
                    progress.bar()
                    if execute(cmd, cwd):
                        developer_languages_built.add(language.name)
                    else:
                        progress.clear()
                        logger.error(
                            f"Failed building {yellow(language.name)} by developer {yellow(developer.username)} for challenge {green(challenge.key)}"
                        )
                        progress.error()

                languages_built.add(language.name)
                progress.clear()

            developer.languages = list(developer_languages_built)
            languages = languages.union(developer_languages_built)

        challenge.languages.sort(key=lambda language: language.name)
