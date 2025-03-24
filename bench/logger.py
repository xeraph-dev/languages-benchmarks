#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import logging
import os
import time
from pathlib import Path

from .colors import blue, clear, green, magenta, red, yellow


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


class FileFormatter(Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return clear(super().format(record))


def create_logger(verbose: int) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(50 - verbose * 10)
    fmt = "%(datetime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    formatter = Formatter(fmt)
    file_formatter = FileFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logs_path = Path(os.getcwd()).joinpath(".logs", "logs.log")
    if not logs_path.exists():
        logs_path.parent.mkdir()
    fh = logging.FileHandler(logs_path)
    fh.setFormatter(file_formatter)
    logger.addHandler(fh)

    return logger
