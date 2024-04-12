from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence

from bench.colors import green, red, yellow
from bench.config import Challenge, ChallengeDeveloper, ChallengeLevel, Config
from bench.locale import _


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


class ArgParser:
    parser: ArgumentParser
    args: Any
    config: Config
    logger: Logger

    def __init__(self, config: Config) -> None:
        self.config = config

        self.parser = ArgumentParser(
            prog="bench", description=_("Run languages benchmarks")
        )

        self.setup()
        self.parse()

    def parse(self) -> None:
        self.args = self.parser.parse_args()

        self.array_it()
        self.sort()
        self.sum_verbose()

    def array_it(self) -> None:
        self.args.challenges = array_it(self.args.challenges)
        self.args.languages = array_it(self.args.languages)
        self.args.developers = array_it(self.args.developers)
        if "levels" in self.args:
            self.args.levels = array_it(self.args.levels)

    def sort(self) -> None:
        self.args.challenges.sort()
        self.args.languages.sort()
        self.args.developers.sort()
        if "levels" in self.args:
            self.args.levels.sort()

    def sum_verbose(self) -> None:
        if "verbose_challenge" in self.args:
            self.args.verbose += self.args.verbose_challenge
            del self.args.verbose_challenge  # type: ignore
        if "verbose_level" in self.args:
            self.args.verbose += self.args.verbose_level
            del self.args.verbose_level  # type: ignore
        if "verbose_language" in self.args:
            self.args.verbose += self.args.verbose_language
            del self.args.verbose_language  # type: ignore
        if "verbose_developer" in self.args:
            self.args.verbose += self.args.verbose_developer
            del self.args.verbose_developer  # type: ignore

    # region setup
    def setup(self) -> None:
        verbose_description = _("increase output verbosity")
        challenges_description = _("Benchmark chosen challenges")
        developers_description = _("Benchmark chosen developers")
        languages_description = _("Benchmark chosen languages")

        self.parser.add_argument(
            "-v",
            "--verbose",
            help=verbose_description,
            action="count",
            dest="verbose",
            default=1,
        )

        self.parser.add_argument(
            "-c",
            "--challenges",
            help=challenges_description,
            type=str,
            action=SplitArgs,
            default=list(self.config.challenges.keys()),
        )

        self.parser.add_argument(
            "-d",
            "--developers",
            help=developers_description,
            type=str,
            action=SplitArgs,
            default=list(self.config.developers.keys()),
        )

        self.parser.add_argument(
            "-L",
            "--languages",
            help=languages_description,
            type=str,
            action=SplitArgs,
            default=list(self.config.languages.keys()),
        )

        subparsers = self.parser.add_subparsers(title="challenges", dest="challenges")
        for challenge in self.config.challenges.values():
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
                        default=list(
                            map(lambda dev: dev.username, challenge.developers)
                        ),
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

    # region check
    def check(self) -> list[Challenge]:
        self.logger.info("Validating command line arguments")

        challenges = list[Challenge]()

        self.check_challenges()

        for challenge in self.config.challenges.values():
            if challenge.key not in self.args.challenges:
                continue

            challenges.append(challenge)
            self.logger.info(f"Included challenge {green(challenge.key)}")

            self.check_levels(challenge)
            self.set_levels(challenge)

            self.check_languages(challenge)
            self.set_languages(challenge)

            self.check_developers(challenge)
            self.set_developers(challenge)

        return challenges

    def check_challenges(self) -> None:
        self.logger.info("Validating challenges")

        for challenge in self.args.challenges:
            if challenge in self.config.challenges.keys():
                continue

            challenges_str = ", ".join(map(yellow, self.config.challenges.keys()))
            self.logger.fatal(
                f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
            )
            exit(1)

    def check_levels(self, challenge: Challenge) -> None:
        self.logger.info(f"Validating levels of the challenge {green(challenge.key)}")

        if "levels" not in self.args:
            return

        for level in self.args.levels:
            level_list = list(map(str, range(1, len(challenge.levels) + 1)))
            if level in level_list:
                continue

            levels_str = ", ".join(map(yellow, level_list))
            self.logger.fatal(
                f"Invalid level, got {red(level)}, expect some of [{levels_str}]"
            )
            exit(1)

    def check_languages(self, challenge: Challenge) -> None:
        self.logger.info(
            f"Validating languages of the challenge {green(challenge.key)}"
        )

        for language in self.args.languages:
            if language in challenge.languages:
                continue

            language_str = ", ".join(map(yellow, self.config.languages.keys()))
            self.logger.fatal(
                f"Invalid language, got {red(language)}, expect some of [{language_str}]"
            )
            exit(1)

    def check_developers(self, challenge: Challenge) -> None:
        self.logger.info(
            f"Validating developers of the challenge {green(challenge.key)}"
        )

        for developer in self.args.developers:
            developer_list = list(map(lambda dev: dev.username, challenge.developers))
            if developer in developer_list:
                continue

            developer_str = ", ".join(
                map(lambda dev: yellow(dev.username), challenge.developers)
            )
            self.logger.fatal(
                f"Invalid developer, got {red(developer)}, expect some of [{developer_str}]"
            )
            exit(1)

    def set_levels(self, challenge: Challenge):
        levels = list[ChallengeLevel]()
        for level in challenge.levels:
            level_index = str(challenge.levels.index(level) + 1)
            if "levels" in self.args and level_index not in self.args.levels:
                continue
            levels.append(level)
        challenge.levels = levels
        levels_str = ", ".join(map(lambda level: yellow(level.name), levels))
        self.logger.info(
            f"Included levels [{levels_str}] in the challenge {green(challenge.key)}"
        )

    def set_languages(self, challenge: Challenge):
        languages = list[str]()
        for language in challenge.languages:
            if language not in self.args.languages:
                continue
            languages.append(language)
        challenge.languages = languages
        languages_str = ", ".join(map(yellow, languages))
        self.logger.info(
            f"Included languages [{languages_str}] in the challenge {green(challenge.key)}"
        )

    def set_developers(self, challenge: Challenge):
        developers = list[ChallengeDeveloper]()
        for developer in challenge.developers:
            if developer.username not in self.args.developers:
                continue
            developers.append(developer)
        challenge.developers = developers
        developers_str = ", ".join(
            map(lambda developer: yellow(developer.username), developers)
        )
        self.logger.info(
            f"Included developers [{developers_str}] in the challenge {green(challenge.key)}"
        )
