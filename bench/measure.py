from logging import Logger

from bench.benchmark import BenchmarkStats


def measure(logger: Logger, stats: list[BenchmarkStats]) -> None:
    print(stats)
    pass
