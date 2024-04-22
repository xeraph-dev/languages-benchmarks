#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os

from .args import parse_args
from .benchmark import benchmark
from .builder import build_challenges
from .config import Config
from .measure import measure
from .printer import print_measures

config = Config(os.path.join(os.getcwd(), "bench.toml"))
logger, challenges = parse_args(config)
build_challenges(logger, config, challenges)
stats = benchmark(logger, config, challenges)
measures = measure(config, stats)
print_measures(measures)
