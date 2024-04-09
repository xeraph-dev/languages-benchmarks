import logging
import time

from bench.colors import blue, green, magenta, red, yellow


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

        record.datetime = magenta(time.strftime(self.default_time_format))

        record.filename = green(record.filename)
        record.lineno = yellow(str(record.lineno))  # type: ignore

        return super().format(record)


def Logger(verbose: int) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(50 - verbose * 10)
    logger.isEnabledFor
    formatter = Formatter(
        "%(datetime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
