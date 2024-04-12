from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence

from bench.colors import green, red, yellow
from bench.config import Challenge, ChallengeDeveloper, ChallengeLevel, Config


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
            prog="bench", description="Run languages benchmarks"
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
        self.parser.add_argument(
            "-v",
            "--verbose",
            help="increase output verbosity",
            action="count",
            dest="verbose",
            default=1,
        )

        self.parser.add_argument(
            "-c",
            "--challenges",
            help="Benchmark chosen challenges, separated by comma",
            type=str,
            action=SplitArgs,
            default=list(self.config.challenges.keys()),
        )

        self.parser.add_argument(
            "-d",
            "--developers",
            help="Benchmark chosen developers, separated by comma",
            type=str,
            action=SplitArgs,
            default=list(self.config.developers.keys()),
        )

        self.parser.add_argument(
            "-L",
            "--languages",
            help="Benchmark chosen languages, separated by comma",
            type=str,
            action=SplitArgs,
            default=list(self.config.languages.keys()),
        )

        subparsers = self.parser.add_subparsers(title="challenges", dest="challenges")
        for challenge in self.config.challenges.values():
            challenge_description = f"Benchmark challenge {green(challenge.name)}"

            challenge_parser = subparsers.add_parser(
                challenge.key,
                help=challenge_description,
                description=challenge_description,
            )

            challenge_parser.add_argument(
                "-v",
                "--verbose",
                help="increase output verbosity",
                action="count",
                dest="verbose_challenge",
                default=0,
            )

            challenge_parser.add_argument(
                "-l",
                "--levels",
                help=f"Benchmark chosen levels of challenge {green(challenge.name)}, separated by comma",
                type=str,
                action=SplitArgs,
                default=list(map(str, range(1, len(challenge.levels) + 1))),
            )

            challenge_parser.add_argument(
                "-L",
                "--languages",
                help=f"Benchmark chosen languages of challenge {green(challenge.name)}, separated by comma",
                type=str,
                action=SplitArgs,
                default=challenge.languages,
            )

            challenge_parser.add_argument(
                "-d",
                "--developers",
                help=f"Benchmark chosen developers of challenge {green(challenge.name)}, separated by comma",
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
                level_description = f"Benchmark level {green(level.name)} of challenge {green(challenge.name)}"

                level_parser = challenge_subparsers.add_parser(
                    str(level_index),
                    help=level_description,
                    description=level_description,
                )

                level_parser.add_argument(
                    "-v",
                    "--verbose",
                    help="increase output verbosity",
                    action="count",
                    dest="verbose_level",
                    default=0,
                )

                level_parser.add_argument(
                    "-L",
                    "--languages",
                    help=f"Benchmark chosen languages in level {green(level.name)} of challenge {green(challenge.name)}",
                    type=str,
                    action=SplitArgs,
                    default=challenge.languages,
                )

                level_parser.add_argument(
                    "-d",
                    "--developers",
                    help=f"Benchmark chosen developers of challenge {green(challenge.name)}, separated by comma",
                    type=str,
                    action=SplitArgs,
                    default=list(map(lambda dev: dev.username, challenge.developers)),
                )

                level_subparsers = level_parser.add_subparsers(
                    title="languages", dest="languages"
                )

                for language in challenge.languages:
                    language_description = f"Benchmark language {language} in level {level.name} of challenge {challenge.name}"

                    language_parser = level_subparsers.add_parser(
                        language,
                        help=language_description,
                        description=level_description,
                    )

                    language_parser.add_argument(
                        "-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="count",
                        dest="verbose_language",
                        default=0,
                    )

                    language_parser.add_argument(
                        "-d",
                        "--developers",
                        help=f"Benchmark chosen developers of challenge {green(challenge.name)}, separated by comma",
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
                        developer_description = f"Benchmark developer {developer} in language {language} in level {level.name} of challenge {challenge.name}"

                        developer_parser = language_subparsers.add_parser(
                            developer.username,
                            help=developer_description,
                            description=developer_description,
                        )

                        developer_parser.add_argument(
                            "-v",
                            "--verbose",
                            help="increase output verbosity",
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

            self.check_levels(challenge)
            self.check_languages(challenge)
            self.check_developers(challenge)

            self.set_levels(challenge)
            self.set_languages(challenge)
            self.set_developers(challenge)

        return challenges

    def check_challenges(self) -> None:
        for challenge in self.args.challenges:
            if challenge in self.config.challenges.keys():
                continue

            challenges_str = ", ".join(map(yellow, self.config.challenges.keys()))
            self.logger.fatal(
                f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
            )
            exit(1)

    def check_levels(self, challenge: Challenge) -> None:
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
        for language in self.args.languages:
            if language in challenge.languages:
                continue

            language_str = ", ".join(map(yellow, self.config.languages.keys()))
            self.logger.fatal(
                f"Invalid language, got {red(language)}, expect some of [{language_str}]"
            )
            exit(1)

    def check_developers(self, challenge: Challenge) -> None:
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

    def set_languages(self, challenge: Challenge):
        languages = list[str]()
        for language in challenge.languages:
            if language not in self.args.languages:
                continue
            languages.append(language)
        challenge.languages = languages

    def set_developers(self, challenge: Challenge):
        developers = list[ChallengeDeveloper]()
        for developer in challenge.developers:
            if developer.username not in self.args.developers:
                continue
            developers.append(developer)
        challenge.developers = developers
