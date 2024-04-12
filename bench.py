import os

from bench.args import ArgParser
from bench.config import Config
from bench.logger import Logger

config = Config(os.path.join(os.getcwd(), "bench.toml"))

args = ArgParser(config)
logger = Logger(args.args.verbose)
args.logger = logger
challenges = args.check()

print(challenges)

# Builder(logger, challenges).build()

# benchmark = Benchmark(logger, config, challenges)
# benchmark.run()
# benchmark.print()
