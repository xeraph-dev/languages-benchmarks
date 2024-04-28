#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence, Tuple

from .colors import green, red, yellow
from .config import (
    Challenge,
    ChallengeDeveloper,
    ChallengeLanguage,
    ChallengeLevel,
    Config,
)
from .logger import create_logger


def array_it(obj: Any | list[Any]):
    return obj if isinstance(obj, list) else [obj]


class SplitArgs(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if isinstance(values, str):
            value_list = list(filter(lambda x: x != "", values.split(",")))
            return setattr(namespace, self.dest, value_list)
        super.__call__(parser, namespace, values, option_string)


# region setup
def setup(parser: ArgumentParser, config: Config) -> None:
    verbose_description = "increase output verbosity"
    challenges_description = "Benchmark chosen challenges"
    developers_description = "Benchmark chosen developers"
    languages_description = "Benchmark chosen languages"

    parser.add_argument(
        "-v",
        "--verbose",
        help=verbose_description,
        action="count",
        dest="verbose",
        default=1,
    )

    parser.add_argument(
        "-c",
        "--challenges",
        help=challenges_description,
        type=str,
        action=SplitArgs,
        default=list(config.challenges.keys()),
    )

    parser.add_argument(
        "-d",
        "--developers",
        help=developers_description,
        type=str,
        action=SplitArgs,
        default=list(config.developers.keys()),
    )

    parser.add_argument(
        "-L",
        "--languages",
        help=languages_description,
        type=str,
        action=SplitArgs,
        default=list(config.languages.keys()),
    )

    subparsers = parser.add_subparsers(title="challenges", dest="challenges")
    for challenge in config.challenges.values():
        challenge_description = f"Benchmark challenge {green(challenge.name)}"
        challenge_developers_description = f"Benchmark chosen developers of challenge {green(challenge.name)}, separated by comma"
        challenge_levels_description = f"Benchmark chosen levels of challenge {green(challenge.name)}, separated by comma"
        challenge_languages_description = f"Benchmark chosen languages of challenge {green(challenge.name)}, separated by comma"

        challenge_parser = subparsers.add_parser(
            challenge.key,
            help=challenge_description,
            description=challenge_description,
        )

        challenge_parser.add_argument(
            "-v",
            "--verbose",
            help=verbose_description,
            action="count",
            dest="verbose_challenge",
            default=0,
        )

        challenge_parser.add_argument(
            "-l",
            "--levels",
            help=challenge_levels_description,
            type=str,
            action=SplitArgs,
            default=list(map(str, range(1, len(challenge.levels) + 1))),
        )

        challenge_parser.add_argument(
            "-L",
            "--languages",
            help=challenge_languages_description,
            type=str,
            action=SplitArgs,
            default=list(map(lambda language: language.name, challenge.languages)),
        )

        challenge_parser.add_argument(
            "-d",
            "--developers",
            help=challenge_developers_description,
            type=str,
            action=SplitArgs,
            default=list(map(lambda dev: dev.username, challenge.developers)),
        )

        challenge_subparsers = challenge_parser.add_subparsers(
            title="levels", dest="levels"
        )
        for level_index, level in zip(
            range(1, len(challenge.levels) + 1), challenge.levels
        ):
            challenge_level_description = f"Benchmark level {green(level.name)} of challenge {green(challenge.name)}"

            level_parser = challenge_subparsers.add_parser(
                str(level_index),
                help=challenge_level_description,
                description=challenge_level_description,
            )

            level_parser.add_argument(
                "-v",
                "--verbose",
                help=verbose_description,
                action="count",
                dest="verbose_level",
                default=0,
            )

            level_parser.add_argument(
                "-L",
                "--languages",
                help=challenge_languages_description,
                type=str,
                action=SplitArgs,
                default=list(map(lambda language: language.name, challenge.languages)),
            )

            level_parser.add_argument(
                "-d",
                "--developers",
                help=challenge_developers_description,
                type=str,
                action=SplitArgs,
                default=list(map(lambda dev: dev.username, challenge.developers)),
            )

            level_subparsers = level_parser.add_subparsers(
                title="languages", dest="languages"
            )

            for language in challenge.languages:
                challenge_language_description = f"Benchmark language {green(language.name)} of challenge {green(challenge.name)}"

                language_parser = level_subparsers.add_parser(
                    language.name,
                    help=challenge_language_description,
                    description=challenge_language_description,
                )

                language_parser.add_argument(
                    "-v",
                    "--verbose",
                    help=verbose_description,
                    action="count",
                    dest="verbose_language",
                    default=0,
                )

                language_parser.add_argument(
                    "-d",
                    "--developers",
                    help=challenge_developers_description,
                    type=str,
                    action=SplitArgs,
                    default=list(map(lambda dev: dev.username, challenge.developers)),
                )

                language_subparsers = language_parser.add_subparsers(
                    title="developers", dest="developers"
                )

                for developer in challenge.developers:
                    challenge_developer_description = f"Benchmark developer {green(developer.username)} of challenge {green(challenge.name)}"

                    developer_parser = language_subparsers.add_parser(
                        developer.username,
                        help=challenge_developer_description,
                        description=challenge_developer_description,
                    )

                    developer_parser.add_argument(
                        "-v",
                        "--verbose",
                        help=verbose_description,
                        action="count",
                        dest="verbose_language",
                        default=0,
                    )


def parse(parser: ArgumentParser) -> Namespace:
    args = parser.parse_args()

    args.challenges = array_it(args.challenges)
    args.languages = array_it(args.languages)
    args.developers = array_it(args.developers)
    if "levels" in args:
        args.levels = array_it(args.levels)

    args.challenges.sort()
    args.languages.sort()
    args.developers.sort()
    if "levels" in args:
        args.levels.sort()

    if "verbose_challenge" in args:
        args.verbose += args.verbose_challenge
        del args.verbose_challenge  # type: ignore
    if "verbose_level" in args:
        args.verbose += args.verbose_level
        del args.verbose_level  # type: ignore
    if "verbose_language" in args:
        args.verbose += args.verbose_language
        del args.verbose_language  # type: ignore
    if "verbose_developer" in args:
        args.verbose += args.verbose_developer
        del args.verbose_developer  # type: ignore

    return args


# region check
def check(logger: Logger, config: Config, args: Namespace) -> list[Challenge]:
    challenges = list[Challenge]()

    check_challenges(logger, config, args)

    for challenge in config.challenges.values():
        if challenge.key not in args.challenges:
            continue

        challenges.append(challenge)
        logger.info(f"Challenge {challenge} included")

        check_levels(challenge, logger, args)
        set_levels(challenge, logger, args)

        check_languages(challenge, logger, config, args)
        set_languages(challenge, logger, args)

        check_developers(challenge, logger, args)
        set_developers(challenge, logger, args)

    return challenges


def check_challenges(logger: Logger, config: Config, args: Namespace) -> None:
    for challenge in args.challenges:
        if challenge in config.challenges.keys():
            continue

        challenges_str = ", ".join(map(yellow, config.challenges.keys()))
        logger.fatal(
            f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
        )
        exit(1)


def check_levels(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    if "levels" not in args:
        return

    for level in args.levels:
        level_list = list(map(str, range(1, len(challenge.levels) + 1)))
        if level in level_list:
            continue

        levels_str = ", ".join(map(yellow, level_list))
        logger.fatal(f"Invalid level, got {red(level)}, expect some of [{levels_str}]")
        exit(1)


def check_languages(
    challenge: Challenge, logger: Logger, config: Config, args: Namespace
) -> None:
    if "levels" not in args:
        return

    for language in args.languages:
        language_list = list(map(lambda language: language.name, challenge.languages))
        if not challenge.languages or language in language_list:
            continue

        language_str = ", ".join(map(yellow, config.languages.keys()))
        logger.fatal(
            f"Invalid language, got {red(language)}, expect some of [{language_str}]"
        )
        exit(1)


def check_developers(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    if "levels" not in args:
        return

    for developer in args.developers:
        developer_list = list(map(lambda dev: dev.username, challenge.developers))
        if developer in developer_list:
            continue

        developer_str = ", ".join(
            map(lambda dev: yellow(dev.username), challenge.developers)
        )
        logger.fatal(
            f"Invalid developer, got {red(developer)}, expect some of [{developer_str}]"
        )
        exit(1)


def set_levels(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    levels = list[ChallengeLevel]()
    for level in challenge.levels:
        level_index = str(challenge.levels.index(level) + 1)
        if "levels" in args and level_index not in args.levels:
            continue
        levels.append(level)
    challenge.levels = levels
    levels_str = ", ".join(map(format, levels))
    logger.info(f"Challenge {challenge}'s levels [{levels_str}] included")


def set_languages(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    languages = list[ChallengeLanguage]()
    for language in challenge.languages:
        if language.name not in args.languages:
            continue
        languages.append(language)
    challenge.languages = languages
    languages_str = ", ".join(map(format, languages))
    logger.info(f"Challenge {challenge}'s languages [{languages_str}] included")


def set_developers(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    developers = list[ChallengeDeveloper]()
    for developer in challenge.developers:
        if developer.username not in args.developers:
            continue
        for language in developer.languages:
            if language not in args.languages:
                continue
            developers.append(developer)
            break
    challenge.developers = developers
    developers_str = ", ".join(map(format, developers))
    logger.info(f"Challenge {challenge}'s developers [{developers_str}] included")


def parse_args(config: Config) -> Tuple[Logger, list[Challenge]]:
    parser = ArgumentParser(prog="bench", description="Run languages benchmarks")
    setup(parser, config)
    args = parse(parser)
    logger = create_logger(args.verbose)
    challenges = check(logger, config, args)
    return logger, challenges
