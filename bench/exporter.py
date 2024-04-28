#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os
from pathlib import Path

from .colors import green
from .measure import ChallengeMeasure


def export_markdown(measures: dict[str, ChallengeMeasure]):
    path = Path(os.path.join(os.getcwd(), "bench.md"))

    md = "# Benchmark results\n\n"

    challenges = list(measures.values())
    for challenge in challenges:
        md += f"## {str(challenge.name)}\n\n"

        levels = challenge.levels.values()
        for level in levels:
            md += f"### {str(level.name)}\n\n"

            md += "| Language | Developer | Mean | Min | Max | Relative | Runs |\n"
            md += "| -------- | --------- | ----: | ---: | ---: | -------: | ---- |\n"

            level.stats.sort(key=lambda stat: stat.mean.base)
            for stat in level.stats:
                summary = list(
                    filter(
                        lambda summ: summ.language == stat.language
                        and summ.developer == stat.developer,
                        level.summary,
                    )
                )[0]
                relative = (
                    "1"
                    if summary == level.summary[0]
                    else f"{summary.mean:.1f}&#160;±&#160;{summary.stdev:.1f}"
                )
                md += f"| {str(stat.language)} | {str(stat.developer)} | {str(stat.mean).strip(" ")}&#160;±&#160;{str(stat.stdev).strip(" ")} | {str(stat.min).strip(" ")} | {str(stat.max).strip(" ")} | {relative} | {stat.successes}/{stat.fails}/{stat.timeouts}/{stat.skips} |\n"

    with open(path, "w") as fp:
        fp.write(md)
    print(f"Benchmarks exported to {green(path.name)}")
