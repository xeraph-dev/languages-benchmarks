import os

from bench.args import parse_args
from bench.benchmark import benchmark
from bench.builder import build_challenges
from bench.config import Config
from bench.measure import measure

config = Config(os.path.join(os.getcwd(), "bench.toml"))
logger, challenges = parse_args(config)
build_challenges(logger, config, challenges)
stats = benchmark(logger, config, challenges)
measure(logger, stats)
