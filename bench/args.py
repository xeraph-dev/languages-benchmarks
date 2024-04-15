from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence, Tuple

from bench.colors import green, red, yellow
from bench.config import Challenge, ChallengeDeveloper, ChallengeLevel, Config
from bench.locales import _
from bench.logger import create_logger


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
    verbose_description = _("increase output verbosity")
    challenges_description = _("Benchmark chosen challenges")
    developers_description = _("Benchmark chosen developers")
    languages_description = _("Benchmark chosen languages")

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
        # challenge_description = f"Benchmark challenge {green(challenge.name)}"
        challenge_description = _("Benchmark challenge") % {
            "challenge": green(challenge.name)
        }
        challenge_developers_description = _(
            "Benchmark chosen developers of challenge"
        ) % {"challenge": green(challenge.name)}
        challenge_levels_description = _("Benchmark chosen levels of challenge") % {
            "challenge": green(challenge.name)
        }
        challenge_languages_description = _(
            "Benchmark chosen languages of challenge"
        ) % {"challenge": green(challenge.name)}

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
            default=challenge.languages,
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
            challenge_level_description = _("Benchmark level of challenge") % {
                "level": green(level.name),
                "challenge": green(challenge.name),
            }

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
                default=challenge.languages,
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
                challenge_language_description = _(
                    "Benchmark language of challenge"
                ) % {
                    "language": green(language),
                    "challenge": green(challenge.name),
                }

                language_parser = level_subparsers.add_parser(
                    language,
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
                    challenge_developer_description = _(
                        "Benchmark developer of challenge"
                    ) % {
                        "developer": green(developer.username),
                        "challenge": green(challenge.name),
                    }

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
    logger.info("Validating command line arguments")

    challenges = list[Challenge]()

    check_challenges(logger, config, args)

    for challenge in config.challenges.values():
        if challenge.key not in args.challenges:
            continue

        challenges.append(challenge)
        logger.info(f"Included challenge {green(challenge.key)}")

        check_levels(challenge, logger, args)
        set_levels(challenge, logger, args)

        check_languages(challenge, logger, config, args)
        set_languages(challenge, logger, args)

        check_developers(challenge, logger, args)
        set_developers(challenge, logger, args)

    return challenges


def check_challenges(logger: Logger, config: Config, args: Namespace) -> None:
    logger.info("Validating challenges")

    for challenge in args.challenges:
        if challenge in config.challenges.keys():
            continue

        challenges_str = ", ".join(map(yellow, config.challenges.keys()))
        logger.fatal(
            f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
        )
        exit(1)


def check_levels(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    logger.info(f"Validating levels of the challenge {green(challenge.key)}")

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
    logger.info(f"Validating languages of the challenge {green(challenge.key)}")

    for language in args.languages:
        if not challenge.languages or language in challenge.languages:
            continue

        language_str = ", ".join(map(yellow, config.languages.keys()))
        logger.fatal(
            f"Invalid language, got {red(language)}, expect some of [{language_str}]"
        )
        exit(1)


def check_developers(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    logger.info(f"Validating developers of the challenge {green(challenge.key)}")

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
    levels_str = ", ".join(map(lambda level: yellow(level.name), levels))
    logger.info(
        f"Included levels [{levels_str}] in the challenge {green(challenge.key)}"
    )


def set_languages(challenge: Challenge, logger: Logger, args: Namespace) -> None:
    languages = list[str]()
    for language in challenge.languages:
        if language not in args.languages:
            continue
        languages.append(language)
    challenge.languages = languages
    languages_str = ", ".join(map(yellow, languages))
    logger.info(
        f"Included languages [{languages_str}] in the challenge {green(challenge.key)}"
    )


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
    developers_str = ", ".join(
        map(lambda developer: yellow(developer.username), developers)
    )
    logger.info(
        f"Included developers [{developers_str}] in the challenge {green(challenge.key)}"
    )


def parse_args(config: Config) -> Tuple[Logger, list[Challenge]]:
    parser = ArgumentParser(prog="bench", description=_("Run languages benchmarks"))
    setup(parser, config)
    args = parse(parser)
    logger = create_logger(args.verbose)
    challenges = check(logger, config, args)
    return logger, challenges
