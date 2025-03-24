#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import unittest

from ..colors import (
    BGBLACK,
    bgblack,
    BGBLUE,
    bgblue,
    BGCYAN,
    bgcyan,
    BGGRAY,
    bggray,
    BGGREEN,
    bggreen,
    BGMAGENTA,
    bgmagenta,
    BGRED,
    bgred,
    BGWHITE,
    bgwhite,
    BGYELLOW,
    bgyellow,
    BLACK,
    black,
    BLUE,
    blue,
    BRIGHT,
    bright,
    clear,
    CYAN,
    cyan,
    DIM,
    dim,
    GRAY,
    gray,
    GREEN,
    green,
    HIDDEN,
    hidden,
    MAGENTA,
    magenta,
    RED,
    red,
    RESET,
    reset,
    REVERSE,
    reverse,
    UNDERSCORE,
    underscore,
    WHITE,
    white,
    YELLOW,
    yellow,
)


class TestColors(unittest.TestCase):
    def test_clear(self) -> None:
        self.assertEqual(
            clear(
                bggray(
                    f"{blue("complex")} foreground {bgmagenta(f"and {red("background")}")} color"
                )
            ),
            "complex foreground and background color",
        )

    def test_reset(self) -> None:
        self.assertEqual(reset("test"), f"test{RESET}")

    def test_bright(self) -> None:
        self.assertEqual(bright("test"), f"{BRIGHT}test{RESET}")

    def test_dim(self) -> None:
        self.assertEqual(dim("test"), f"{DIM}test{RESET}")

    def test_underscore(self) -> None:
        self.assertEqual(underscore("test"), f"{UNDERSCORE}test{RESET}")

    def test_reverse(self) -> None:
        self.assertEqual(reverse("test"), f"{REVERSE}test{RESET}")

    def test_hidden(self) -> None:
        self.assertEqual(hidden("test"), f"{HIDDEN}test{RESET}")

    def test_black(self) -> None:
        self.assertEqual(black("test"), f"{BLACK}test{RESET}")

    def test_red(self) -> None:
        self.assertEqual(red("test"), f"{RED}test{RESET}")

    def test_green(self) -> None:
        self.assertEqual(green("test"), f"{GREEN}test{RESET}")

    def test_yellow(self) -> None:
        self.assertEqual(yellow("test"), f"{YELLOW}test{RESET}")

    def test_blue(self) -> None:
        self.assertEqual(blue("test"), f"{BLUE}test{RESET}")

    def test_magenta(self) -> None:
        self.assertEqual(magenta("test"), f"{MAGENTA}test{RESET}")

    def test_cyan(self) -> None:
        self.assertEqual(cyan("test"), f"{CYAN}test{RESET}")

    def test_white(self) -> None:
        self.assertEqual(white("test"), f"{WHITE}test{RESET}")

    def test_gray(self) -> None:
        self.assertEqual(gray("test"), f"{GRAY}test{RESET}")

    def test_bgblack(self) -> None:
        self.assertEqual(bgblack("test"), f"{BGBLACK}test{RESET}")

    def test_bgred(self) -> None:
        self.assertEqual(bgred("test"), f"{BGRED}test{RESET}")

    def test_bggreen(self) -> None:
        self.assertEqual(bggreen("test"), f"{BGGREEN}test{RESET}")

    def test_bgyellow(self) -> None:
        self.assertEqual(bgyellow("test"), f"{BGYELLOW}test{RESET}")

    def test_bgblue(self) -> None:
        self.assertEqual(bgblue("test"), f"{BGBLUE}test{RESET}")

    def test_bgmagenta(self) -> None:
        self.assertEqual(bgmagenta("test"), f"{BGMAGENTA}test{RESET}")

    def test_bgcyan(self) -> None:
        self.assertEqual(bgcyan("test"), f"{BGCYAN}test{RESET}")

    def test_bgwhite(self) -> None:
        self.assertEqual(bgwhite("test"), f"{BGWHITE}test{RESET}")

    def test_bggray(self) -> None:
        self.assertEqual(bggray("test"), f"{BGGRAY}test{RESET}")


class TestColorsEdgeCases(unittest.TestCase):
    def test_avoid_multiple_reset(self) -> None:
        self.assertEqual(reset(reset("test")), f"test{RESET}")

    def test_over_reset_color(self) -> None:
        self.assertEqual(reset(red("test")), f"{RED}test{RESET}")

    def test_restore_current_color(self) -> None:
        self.assertEqual(
            dim(f"test {red("restored")} correctly"),
            f"{DIM}test {RED}restored{RESET}{DIM} correctly{RESET}",
        )

    def test_multiple_restore_current_color(self) -> None:
        self.assertEqual(
            bggray(f"{blue("complex")} test {red("restored")} correctly"),
            f"{BGGRAY}{BLUE}complex{RESET}{BGGRAY} test {RED}restored{RESET}{BGGRAY} correctly{RESET}",
        )

    def test_multiple_foreground_and_background_color(self) -> None:
        self.assertEqual(red("background"), f"{RED}background{RESET}")
        self.assertEqual(
            bgmagenta(f"and {red("background")}"),
            f"{BGMAGENTA}and {RED}background{RESET}",
        )
        self.assertEqual(
            bggray(f"foreground {bgmagenta(f"and {red("background")}")} color"),
            f"{BGGRAY}foreground {BGMAGENTA}and {RED}background{RESET}{BGGRAY} color{RESET}",
        )
        self.assertEqual(
            bggray(
                f"{blue("complex")} foreground {bgmagenta(f"and {red("background")}")} color"
            ),
            f"{BGGRAY}{BLUE}complex{RESET}{BGGRAY} foreground {BGMAGENTA}and {RED}background{RESET}{BGGRAY} color{RESET}",
        )


if __name__ == "__main__":
    unittest.main()
