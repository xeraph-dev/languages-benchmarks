#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import importlib
import inspect
import pathlib
import sys
import unittest
from typing import Any

test_cases = list[type[Any]]()

print()

for file in pathlib.Path(__file__).parent.glob("./*_test.py"):
    module = importlib.import_module(
        str(__package__) + "." + file.name.replace(".py", "")
    )
    members = inspect.getmembers(module, inspect.isclass)
    for name, klass in members:
        if klass.__module__ is not module.__name__ or not name.startswith("Test"):
            continue
        test_cases.append(klass)

if __name__ == "__main__":
    verbosity = 2 if "-v" in sys.argv else 1
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite)
