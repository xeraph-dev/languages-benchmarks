#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import sys
import unittest
from argparse import ArgumentParser, Namespace

from ..args import parse, parse_args, setup
from ..tests.utils import load_config, mock_challenge


def just_parse() -> Namespace:
    parser = ArgumentParser()
    config = load_config()
    setup(parser, config)
    args = parse(parser)
    return args


class TestParseArgs(unittest.TestCase):
    def test_parse_args_default(self) -> None:
        sys.argv = sys.argv[0:1]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1", "challenge-2"])
        self.assertTrue("levels" not in args)
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenges(self) -> None:
        sys.argv = sys.argv[0:1] + ["-c", "challenge-1,challenge-2"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1", "challenge-2"])
        self.assertTrue("levels" not in args)
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["1", "2", "3"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge_levels(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-l", "1,3"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["1", "3"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge_languages(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-L", "swift"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["1", "2", "3"])
        self.assertEqual(args.languages, ["swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge_developers(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "-d", "developer-1"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["1", "2", "3"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1"])

    def test_parse_args_challenge_all_flags(self) -> None:
        sys.argv = sys.argv[0:1] + [
            "challenge-1",
            "-l",
            "1,3",
            "-L",
            "swift",
            "-d",
            "developer-1",
        ]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["1", "3"])
        self.assertEqual(args.languages, ["swift"])
        self.assertEqual(args.developers, ["developer-1"])

    def test_parse_args_challenge_level(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge_level_languages(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "-L", "go,swift"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_challenge_level_developers(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "-d", "developer-1"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["go", "swift"])
        self.assertEqual(args.developers, ["developer-1"])

    def test_parse_args_challenge_level_all_flags(self) -> None:
        sys.argv = sys.argv[0:1] + [
            "challenge-1",
            "2",
            "-L",
            "swift",
            "-d",
            "developer-1",
        ]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["swift"])
        self.assertEqual(args.developers, ["developer-1"])

    def test_parse_args_language(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["swift"])
        self.assertEqual(args.developers, ["developer-1", "developer-2"])

    def test_parse_args_developer(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift", "developer-1"]
        args = just_parse()
        self.assertEqual(args.challenges, ["challenge-1"])
        self.assertEqual(args.levels, ["2"])
        self.assertEqual(args.languages, ["swift"])
        self.assertEqual(args.developers, ["developer-1"])


class TestCheckParsedArgs(unittest.TestCase):
    def test_check(self) -> None:
        sys.argv = sys.argv[0:1] + ["challenge-1", "2", "swift", "developer-1"]
        _, challenges = parse_args(load_config())
        self.assertEqual(challenges, [mock_challenge])


if __name__ == "__main__":
    unittest.main()
