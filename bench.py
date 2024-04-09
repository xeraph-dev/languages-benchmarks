import os

from bench.args import ArgParser
from bench.benchmark import Benchmark
from bench.builder import Builder
from bench.config import Config
from bench.logger import Logger

config = Config(os.path.join(os.getcwd(), "bench.toml"))

args = ArgParser(config)
logger = Logger(args.args.verbose)
args.logger = logger
challenges = args.check()

Builder(logger, challenges).build()

benchmark = Benchmark(logger, config, challenges)
# benchmark.run()
# benchmark.print()
