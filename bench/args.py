#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.
from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence, Tuple

from .colors import green, red, yellow
from .config import Challenge, Config
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


def check_challenges(logger: Logger, config: Config, args: Namespace) -> None:
    challenges_range = sorted(config.challenges.keys())
    challenges_str = ", ".join(map(yellow, challenges_range))
    invalid_challenges = set(args.challenges).difference(challenges_range)
    if invalid_challenges:
        logger.fatal(
            f"Invalid challenge, got {red(invalid_challenges.pop())}, expect some of [{challenges_str}]"
        )
        exit(1)


def check_levels(logger: Logger, args: Namespace, challenge: Challenge) -> None:
    if "levels" not in args:
        return

    levels_range = sorted(map(str, range(1, len(challenge.levels) + 1)))
    levels_str = ", ".join(map(yellow, levels_range))
    invalid_levels = set(args.levels).difference(levels_range)
    if invalid_levels:
        logger.fatal(
            f"Invalid level, got {red(invalid_levels.pop())}, expect some of [{levels_str}]"
        )
        exit(1)


def check_languages(
    logger: Logger, config: Config, args: Namespace, challenge: Challenge
) -> None:
    languages_range = sorted(
        map(lambda lang: lang.name, challenge.languages)
        if "levels" in args
        else config.languages.keys()
    )
    languages_str = ", ".join(map(yellow, languages_range))
    invalid_languages = set(args.languages).difference(languages_range)
    if invalid_languages:
        logger.fatal(
            f"Invalid language, got {red(invalid_languages.pop())}, expect some of [{languages_str}]"
        )
        exit(1)


def check_developer(
    logger: Logger, config: Config, args: Namespace, challenge: Challenge
) -> None:
    developers_range = sorted(
        map(lambda dev: dev.username, challenge.developers)
        if "levels" in args
        else config.developers.keys()
    )
    developers_str = ", ".join(map(yellow, developers_range))
    invalid_developers = set(args.developers).difference(developers_range)
    if invalid_developers:
        logger.fatal(
            f"Invalid developer, got {red(invalid_developers.pop())}, expect some of [{developers_str}]"
        )
        exit(1)


def set_levels(args: Namespace, challenge: Challenge) -> None:
    if "levels" not in args:
        return
    levels = []
    [
        levels.append(challenge_level)
        for level in args.levels
        for index, challenge_level in enumerate(challenge.levels)
        if str(index + 1) == level and challenge_level not in levels
    ]
    challenge.levels = levels


def set_languages(args: Namespace, challenge: Challenge) -> None:
    languages = []
    [
        languages.append(challenge_language)
        for language in args.languages
        for developer in args.developers
        for challenge_language in challenge.languages
        for challenge_developer in challenge.developers
        if challenge_language.name == language
        and challenge_developer.username == developer
        and challenge_language.name in challenge_developer.languages
        and challenge_language not in languages
    ]
    challenge.languages = languages


def set_developers(args: Namespace, challenge: Challenge) -> None:
    developers = []
    [
        developers.append(challenge_developer)
        for developer in args.developers
        for challenge_developer in challenge.developers
        for language in challenge_developer.languages
        if challenge_developer.username == developer
        and language in args.languages
        and challenge_developer not in developers
    ]
    challenge.developers = developers


def check(logger: Logger, config: Config, args: Namespace) -> list[Challenge]:
    challenges = list[Challenge]()

    check_challenges(logger, config, args)

    for challenge in config.challenges.values():
        if challenge.key not in args.challenges:
            continue

        check_levels(logger, args, challenge)
        set_levels(args, challenge)

        check_languages(logger, config, args, challenge)
        set_languages(args, challenge)

        check_developer(logger, config, args, challenge)
        set_developers(args, challenge)

        if not challenge.levels or not challenge.languages or not challenge.developers:
            continue

        challenges.append(challenge)
        logger.info(f"Challenge {challenge} included")

        developers_str = ", ".join(map(format, challenge.developers))
        logger.info(f"Challenge {challenge}'s developers [{developers_str}] included")

        levels_str = ", ".join(map(format, challenge.levels))
        logger.info(f"Challenge {challenge}'s levels [{levels_str}] included")

        languages_str = ", ".join(map(format, challenge.languages))
        logger.info(f"Challenge {challenge}'s languages [{languages_str}] included")

    return challenges


def parse_args(config: Config) -> Tuple[Logger, list[Challenge]]:
    parser = ArgumentParser(prog="bench", description="Run languages benchmarks")
    setup(parser, config)
    args = parse(parser)
    logger = create_logger(args.verbose)
    challenges = check(logger, config, args)
    return logger, challenges
