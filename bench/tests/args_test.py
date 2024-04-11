import sys
import unittest

from bench.args import ArgParser
from bench.tests.utils import load_config


class TestArgs(unittest.TestCase):
    def test_init_default(self) -> None:
        sys.argv = sys.argv[0:1]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1", "challenge-2"])
        self.assertNotIn("levels", args.args)
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenges(self) -> None:
        sys.argv = sys.argv[0:1] + ["-c", "challenge-1,challenge-2"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1", "challenge-2"])
        self.assertNotIn("levels", args.args)
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["1", "2", "3"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge_levels(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-l", "1,3"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["1", "3"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge_languages(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-L", "swift"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["1", "2", "3"])
        self.assertEqual(args.args.languages, ["swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge_developers(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-d", "developer-1"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["1", "2", "3"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1"])

    def test_init_challenge_all_flags(self) -> None:
        sys.argv = sys.argv[0:1] + [
            "challenge-1",
            "-l",
            "1,3",
            "-L",
            "swift",
            "-d",
            "developer-1",
        ]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["1", "3"])
        self.assertEqual(args.args.languages, ["swift"])
        self.assertEqual(args.args.developers, ["developer-1"])

    def test_init_challenge_level(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge_level_languages(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "-L", "go,swift"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_challenge_level_developers(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "-d", "developer-1"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["go", "swift"])
        self.assertEqual(args.args.developers, ["developer-1"])

    def test_init_challenge_level_all_flags(self) -> None:
        sys.argv = sys.argv[0:1] + [
            "challenge-1",
            "2",
            "-L",
            "swift",
            "-d",
            "developer-1",
        ]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["swift"])
        self.assertEqual(args.args.developers, ["developer-1"])

    def test_init_language(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["swift"])
        self.assertEqual(args.args.developers, ["developer-1", "developer-2"])

    def test_init_developer(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift", "developer-1"]
        args = ArgParser(load_config())
        self.assertEqual(args.args.challenges, ["challenge-1"])
        self.assertEqual(args.args.levels, ["2"])
        self.assertEqual(args.args.languages, ["swift"])
        self.assertEqual(args.args.developers, ["developer-1"])

    # def test_check(self) -> None:
    #     sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift"]
    #     args = ArgParser(load_config())
    #     args.logger = Logger(args.args.verbose)
    #     challenges = args.check()
    #     self.assertEqual(
    #         challenges,
    #         [
    #             Challenge(
    #                 "challenge-1",
    #                 "Advent of Code - Year 2015 - Day 4",
    #                 [
    #                     Level(
    #                         "2",
    #                         "6 zeros",
    #                         [Language("swift", "swift/.build/release/:challenge")],
    #                         ["yzbqklnj", "6"],
    #                         "9962624",
    #                     )
    #                 ],
    #             )
    #         ],
    #     )


if __name__ == "__main__":
    unittest.main()
