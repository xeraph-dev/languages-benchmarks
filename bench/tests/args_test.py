import sys
import unittest

from bench.args import ArgParser
from bench.config import Challenge, Language, Level
from bench.logger import Logger
from bench.tests.utils import load_config


class TestArgs(unittest.TestCase):
    def test_init_default(self) -> None:
        sys.argv = sys.argv[0:1]
        args = ArgParser(load_config())
        self.assertEqual(
            args.args.challenges, ["aoc-year2015-day4", "aoc-year2020-day15"]
        )
        self.assertNotIn("levels", args.args)
        self.assertNotIn("languages", args.args)

    def test_init_challenge(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, "aoc-year2015-day4")
        self.assertEqual(args.args.levels, ["1", "2", "3"])
        self.assertNotIn("languages", args.args)

    def test_init_challenges(self) -> None:
        sys.argv = sys.argv[0:1] + ["-c", "aoc-year2015-day4,aoc-year2020-day15"]
        args = ArgParser(load_config())
        self.assertEqual(
            args.args.challenges, ["aoc-year2015-day4", "aoc-year2020-day15"]
        )
        self.assertNotIn("levels", args.args)
        self.assertNotIn("languages", args.args)

    def test_init_level(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4", "2"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, "aoc-year2015-day4")
        self.assertEqual(args.args.levels, "2")
        self.assertEqual(args.args.languages, ["go", "swift"])

    def test_init_levels(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4", "-l", "1,3"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, "aoc-year2015-day4")
        self.assertEqual(args.args.levels, ["1", "3"])
        self.assertNotIn("languages", args.args)

    def test_init_language(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4", "2", "swift"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, "aoc-year2015-day4")
        self.assertEqual(args.args.levels, "2")
        self.assertEqual(args.args.languages, "swift")

    def test_init_languages(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4", "2", "-l", "go,swift"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, "aoc-year2015-day4")
        self.assertEqual(args.args.levels, "2")
        self.assertEqual(args.args.languages, ["go", "swift"])

    def test_check(self) -> None:
        sys.argv = sys.argv[0:1] + ["aoc-year2015-day4", "2", "swift"]
        args = ArgParser(load_config())
        args.logger = Logger(args.args.verbose)
        challenges = args.check()
        self.assertEqual(
            challenges,
            [
                Challenge(
                    "aoc-year2015-day4",
                    "Advent of Code - Year 2015 - Day 4",
                    [
                        Level(
                            "2",
                            "6 zeros",
                            [Language("swift", "swift/.build/release/:challenge")],
                            ["yzbqklnj", "6"],
                            "9962624",
                        )
                    ],
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
