#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

from .measure import ChallengeMeasure


def print_measures(measures: dict[str, ChallengeMeasure]) -> None:
    challenges = list(measures.values())
    for challenge in challenges:
        if challenge is not challenges[0]:
            print()
        print(f"\n{challenge}")
