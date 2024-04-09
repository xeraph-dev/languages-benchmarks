import argparse
from logging import Logger
from typing import Any, List

from bench.colors import green, red, yellow
from bench.config import Challenge, Config, Language, Level


def array_it(obj: Any | List[Any]):
    return obj if isinstance(obj, list) else [obj]


class SplitArgs(argparse.Action):
    def __call__(self, parser, namespace, values: str, option_string=None) -> None:
        setattr(namespace, self.dest, values.split(","))


class ArgParser:
    parser: argparse.ArgumentParser
    args: Any
    config: Config
    logger: Logger

    def __init__(self, config: Config) -> None:
        self.config = config

        self.parser = argparse.ArgumentParser(
            prog="bench", description="Run languages benchmarks"
        )

        self.setup()
        self.parse()

    def setup(self) -> None:
        self.parser.add_argument(
            "-v", "--verbose", help="increase output verbosity", action="count"
        )

        self.parser.add_argument(
            "-c",
            "--challenges",
            help="Benchmark chosen challenges, separated by comma",
            type=str,
            action=SplitArgs,
            default=list(map(lambda challenge: challenge.key, self.config.challenges)),
        )

        subparsers = self.parser.add_subparsers(title="challenges", dest="challenges")
        for challenge in self.config.challenges:
            challenge_description = f"Benchmark challenge {green(challenge.name)}"

            challenge_parser = subparsers.add_parser(
                challenge.key,
                help=challenge_description,
                description=challenge_description,
            )

            challenge_parser.add_argument(
                "-l",
                "--levels",
                help=f"Benchmark chosen levels of challenge {green(challenge.name)}, separated by comma",
                type=str,
                action=SplitArgs,
                default=list(map(lambda level: level.level, challenge.levels)),
            )

            challenge_subparsers = challenge_parser.add_subparsers(
                title="levels", dest="levels"
            )
            for level in challenge.levels:
                level_description = f"Benchmark level {green(level.name)} of challenge {green(challenge.name)}"

                level_parser = challenge_subparsers.add_parser(
                    level.level, help=level_description, description=level_description
                )

                level_parser.add_argument(
                    "-l",
                    "--languages",
                    help=f"Benchmark chosen languages in level {green(level.name)} of challenge {green(challenge.name)}",
                    type=str,
                    action=SplitArgs,
                    default=list(map(lambda language: language.name, level.languages)),
                )

                level_subparsers = level_parser.add_subparsers(
                    title="languages", dest="languages"
                )

                for language in level.languages:
                    language_description = f"Benchmark language {language.name} in level {level.name} of challenge {challenge.name}"

                    level_subparsers.add_parser(
                        language.name,
                        help=language_description,
                        description=level_description,
                    )

    def parse(self) -> None:
        self.args = self.parser.parse_args()
        if self.args.verbose is None:
            self.args.verbose = 0
        self.args.verbose += 1

    def check(self) -> List[Challenge]:
        self.logger.info("Validating command line arguments")

        challenges = list[Challenge]()

        self.args.challenges = array_it(self.args.challenges)

        if "levels" in self.args:
            self.args.levels = array_it(self.args.levels)
        if "languages" in self.args:
            self.args.languages = array_it(self.args.languages)

        for challenge in self.args.challenges:
            challenge_list = list(
                map(lambda challenge: challenge.key, self.config.challenges)
            )
            if challenge not in challenge_list:
                challenges_str = ", ".join(map(yellow, challenge_list))
                self.logger.fatal(
                    f"Invalid challenge, got {red(challenge)}, expect some of [{challenges_str}]"
                )
                exit(1)

        for challenge in self.config.challenges:
            if challenge.key not in self.args.challenges:
                continue

            challenges.append(challenge)

            if "levels" in self.args:
                for level in self.args.levels:
                    if level == "":
                        continue

                    levels = list(map(lambda level: level.level, challenge.levels))
                    if level not in levels:
                        levels_str = ", ".join(map(yellow, levels))
                        self.logger.fatal(
                            f"Invalid level, got {red(level)}, expect some of [{levels_str}]"
                        )
                        exit(1)

            levels = list[Level]()

            for level in challenge.levels:
                if "levels" in self.args and level.level not in self.args.levels:
                    continue

                levels.append(level)

                if "languages" in self.args:
                    for language in self.args.languages:
                        languages = list(
                            map(lambda language: language.name, level.languages)
                        )
                        if language not in languages:
                            languages_str = ", ".join(map(yellow, languages))
                            self.logger.fatal(
                                f"Invalid language, got {red(language)}, expect some of [{languages_str}]"
                            )
                            exit(1)

                languages = list[Language]()
                for language in self.config.languages:
                    if (
                        "languages" in self.args
                        and language.name not in self.args.languages
                    ):
                        continue

                    languages.append(language)

                level.languages = languages

            challenge.levels = levels

        return challenges
