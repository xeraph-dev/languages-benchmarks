from argparse import Action, ArgumentParser, Namespace
from logging import Logger
from typing import Any, Sequence

from bench.colors import green
from bench.config import Challenge, Config


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
            return setattr(namespace, self.dest, values.split(","))
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

    def check(self) -> list[Challenge]:
        self.logger.info("Validating command line arguments")

        challenges = list[Challenge]()

        return challenges


# region check
# def check(self) -> List[Challenge]:
#     self.logger.info("Validating command line arguments")

#     challenges = list[Challenge]()

#     for challenge in self.args.challenges:
#         challenge_list = list(
#             map(lambda challenge: challenge.key, self.config.challenges)
#         )
#         if challenge not in challenge_list:
#             challenges_str = ", ".join(map(yellow, challenge_list))
#             self.logger.fatal(
#                 f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
#             )
#             exit(1)

#     for challenge in self.config.challenges:
#         if challenge.key not in self.args.challenges:
#             continue

#         challenges.append(challenge)

#         if "levels" in self.args:
#             for level in self.args.levels:
#                 if level == "":
#                     continue

#                 levels = list(map(lambda level: level.level, challenge.levels))
#                 if level not in levels:
#                     levels_str = ", ".join(map(yellow, levels))
#                     self.logger.fatal(
#                         f"Invalid level, got {red(level)}, expect some of [{levels_str}]"
#                     )
#                     exit(1)

#         levels = list[Level]()

#         for level in challenge.levels:
#             if "levels" in self.args and level.level not in self.args.levels:
#                 continue

#             levels.append(level)

#             if "languages" in self.args:
#                 for language in self.args.languages:
#                     languages = list(
#                         map(lambda language: language.name, level.languages)
#                     )
#                     if language not in languages:
#                         languages_str = ", ".join(map(yellow, languages))
#                         self.logger.fatal(
#                             f"Invalid language, got {red(language)}, expect some of [{languages_str}]"
#                         )
#                         exit(1)

#             languages = list[Language]()
#             for language in self.config.languages:
#                 if (
#                     "languages" in self.args
#                     and language.name not in self.args.languages
#                 ):
#                     continue

#                 languages.append(language)

#             level.languages = languages

#         challenge.levels = levels

#     return challenges
