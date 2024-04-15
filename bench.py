import os

from bench.args import parse_args
from bench.benchmark import benchmark
from bench.builder import build_challenges
from bench.config import Config

config = Config(os.path.join(os.getcwd(), "bench.toml"))
logger, challenges = parse_args(config)
build_challenges(logger, config, challenges)
benchmark(logger, config, challenges)
