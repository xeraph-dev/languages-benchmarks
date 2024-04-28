#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import logging
import time

from .colors import blue, green, magenta, red, yellow


class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        match record.levelname:
            case "DEBUG":
                record.levelname = "DEBU"
            case "INFO":
                record.levelname = blue("INFO")
            case "WARNING":
                record.levelname = yellow("WARN")
            case "CRITICAL":
                record.levelname = red("FATA")
            case "ERROR":
                record.levelname = red("ERRO")
            case _:
                pass

        record.datetime = magenta(time.strftime(self.default_time_format))

        record.filename = green(record.filename)
        record.lineno = yellow(str(record.lineno))  # type: ignore

        return super().format(record)


def create_logger(verbose: int) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(50 - verbose * 10)
    formatter = Formatter(
        "%(datetime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
