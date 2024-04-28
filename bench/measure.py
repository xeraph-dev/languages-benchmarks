#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

from dataclasses import dataclass
from enum import Enum
from statistics import mean, stdev
from typing import Self

from .benchmark import BenchmarkStats
from .colors import dim, green, magenta, yellow
from .config import (
    ChallengeDeveloperName,
    ChallengeLanguageName,
    ChallengeLevelName,
    ChallengeName,
    Config,
)


class TimeName(Enum):
    nanosecond = "nanosecond"
    microsecond = "microsecond"
    millisecond = "millisecond"
    second = "second"
    minute = "minute"
    hour = "hour"

    def prev(self):
        match self:
            case TimeName.nanosecond:
                return TimeName.nanosecond
            case TimeName.microsecond:
                return TimeName.nanosecond
            case TimeName.millisecond:
                return TimeName.microsecond
            case TimeName.second:
                return TimeName.millisecond
            case TimeName.minute:
                return TimeName.second
            case TimeName.hour:
                return TimeName.minute

    def next(self):
        match self:
            case TimeName.nanosecond:
                return TimeName.microsecond
            case TimeName.microsecond:
                return TimeName.millisecond
            case TimeName.millisecond:
                return TimeName.second
            case TimeName.second:
                return TimeName.minute
            case TimeName.minute:
                return TimeName.hour
            case TimeName.hour:
                return TimeName.hour

    def __str__(self) -> str:
        match self:
            case TimeName.nanosecond:
                return "ns"
            case TimeName.microsecond:
                return "μs"
            case TimeName.millisecond:
                return "ms"
            case TimeName.second:
                return "s "
            case TimeName.minute:
                return "m "
            case TimeName.hour:
                return "h "


@dataclass
class TimeMeasure:
    base: float
    unit: float
    name: TimeName

    def __init__(self, base: float, name: TimeName):
        self.base = base
        self.unit = base
        self.name = name

    def adjust(self) -> Self:
        while True:
            match self.name:
                case TimeName.nanosecond if self.unit < 100:
                    return self
                case (
                    TimeName.microsecond | TimeName.millisecond
                ) if 0 <= self.unit < 1000:
                    return self
                case TimeName.second | TimeName.minute if 0 <= self.unit < 60:
                    return self
                case TimeName.hour if self.unit > 0:
                    return self

                case TimeName.nanosecond | TimeName.microsecond | TimeName.millisecond:
                    if self.unit < 0:
                        self.unit *= 1000
                        self.name = self.name.prev()
                    if self.unit >= 1000:
                        self.unit /= 1000
                        self.name = self.name.next()

                case TimeName.second:
                    if self.unit < 0:
                        self.unit *= 1000
                        self.name = self.name.prev()
                    if self.unit > 60:
                        self.unit /= 60
                        self.name = self.name.next()

                case TimeName.minute:
                    if self.unit < 0:
                        self.unit *= 60
                        self.name = self.name.prev()
                    if self.unit > 60:
                        self.unit /= 60
                        self.name = self.name.next()

                case TimeName.hour:
                    if self.unit < 0:
                        self.unit *= 60
                        self.name = self.name.prev()

    def __str__(self) -> str:
        return f"{self.unit: >5.1f}{self.name}".ljust(7)

    def __format__(self, format_spec: str) -> str:
        unit = f"{self.unit: >5.1f}"
        return f"{yellow(unit)}{self.name}"


@dataclass
class MeasureStat:
    successes: int
    fails: int
    timeouts: int
    skips: int
    max: TimeMeasure
    min: TimeMeasure
    mean: TimeMeasure
    stdev: TimeMeasure
    developer: ChallengeDeveloperName
    language: ChallengeLanguageName
    max_language_len: int
    max_developer_len: int

    def __format__(self, format_spec: str) -> str:
        language_space = " " * (self.max_language_len - len(self.language))
        developer_space = " " * (self.max_developer_len - len(self.developer))

        runs = self.successes + self.fails + self.timeouts + self.skips

        data_line = (
            f"{runs} runs - {self.successes}/{self.fails}/{self.timeouts}/{self.skips}"
        )
        data_len = len(data_line)
        line_len = self.max_language_len + self.max_developer_len + 5 + len("by")
        data_line = data_line.rjust((line_len - data_len) // 2 + data_len)
        data_line = data_line.ljust(line_len)

        return f"""\
    {language_space}{self.language} by {self.developer}{developer_space} - {green("mean")} ± {green("σ")}    {self.mean} ± {self.stdev}
    {dim(data_line)} {magenta("min")} … {magenta("max")}  {self.min} … {self.max}\
"""


@dataclass
class ChallengeLevelSummary:
    mean: float
    stdev: float
    developer: ChallengeDeveloperName
    language: ChallengeLanguageName

    def __format__(self, format_spec: str) -> str:
        if format_spec == "faster":
            return f"      {self.language} by {self.developer} ran"

        return f"""      {yellow(f"{self.mean: >5.1f}")} ± {yellow(f"{self.stdev: >4.1f}")} times faster than {self.language} by {self.developer}"""


@dataclass
class ChallengeLevelMeasure:
    name: ChallengeLevelName
    stats: list[MeasureStat]
    summary: list[ChallengeLevelSummary]

    def __init__(self, name: ChallengeLevelName) -> None:
        self.name = name
        self.stats = []
        self.summary = []

    def __format__(self, format_spec: str) -> str:
        return (
            f"{self.name}\n"
            + "\n\n".join([f"{stat}" for stat in self.stats] + ["    Summary\n"])
            + "\n".join(
                [
                    f"{summary:faster}" if summary is self.summary[0] else f"{summary}"
                    for summary in self.summary
                ]
            )
        )


@dataclass
class ChallengeMeasure:
    key: ChallengeName
    name: ChallengeName
    levels: dict[str, ChallengeLevelMeasure]

    def __init__(self, key: ChallengeName, name: ChallengeName) -> None:
        self.key = key
        self.name = name
        self.levels = {}
        self.summary = []

    def __format__(self, format_spec: str) -> str:
        return f"{self.name}\n" + "\n\n".join(
            [f"  {level}" for level in self.levels.values()]
        )


def measure(config: Config, stats: list[BenchmarkStats]) -> dict[str, ChallengeMeasure]:
    measures = dict[str, ChallengeMeasure]()

    max_language_len = max(*[len(stat.language) for stat in stats])
    max_developer_len = max(*[len(stat.developer) for stat in stats])

    for stat in stats:
        times = list(map(lambda m: m.time, stat.measures))
        mean_time = mean(times)

        if stat.challenge not in measures:
            measures[stat.challenge] = ChallengeMeasure(
                stat.challenge, config.challenges[stat.challenge].name
            )

        if stat.level not in measures[stat.challenge].levels:
            measures[stat.challenge].levels[stat.level] = ChallengeLevelMeasure(
                stat.level
            )

        measures[stat.challenge].levels[stat.level].stats.append(
            MeasureStat(
                stat.successes,
                stat.fails,
                stat.timeouts,
                stat.skips,
                TimeMeasure(max(*times), TimeName.nanosecond).adjust(),
                TimeMeasure(min(*times), TimeName.nanosecond).adjust(),
                TimeMeasure(mean_time, TimeName.nanosecond).adjust(),
                TimeMeasure(stdev(times, mean_time), TimeName.nanosecond).adjust(),
                stat.developer,
                stat.language,
                max_language_len,
                max_developer_len,
            )
        )

    for challenge in measures:
        for level in measures[challenge].levels:
            filtered_stats = filter(
                lambda stat: stat.fails + stat.timeouts + stat.skips == 0,
                measures[challenge].levels[level].stats,
            )
            sorted_stats = sorted(filtered_stats, key=lambda stat: stat.mean.base)

            for stat in sorted_stats:
                summary_mean = (
                    stat.mean.base
                    if stat is sorted_stats[0]
                    else stat.mean.base / sorted_stats[0].mean.base
                )

                min_ratio = (
                    stat.min.base
                    if stat is sorted_stats[0]
                    else stat.min.base / sorted_stats[0].min.base
                )

                max_ratio = (
                    stat.max.base
                    if stat is sorted_stats[0]
                    else stat.max.base / sorted_stats[0].max.base
                )

                measures[challenge].levels[level].summary.append(
                    ChallengeLevelSummary(
                        summary_mean,
                        abs(max_ratio - min_ratio),
                        stat.developer,
                        stat.language,
                    )
                )

    return measures
