import unittest
from logging.handlers import MemoryHandler

from bench.logger import create_logger


class TestLoggerVerbosity(unittest.TestCase):
    def log(self, verbose: int) -> MemoryHandler:
        logger = create_logger(verbose)
        ch = MemoryHandler(1024)
        logger.addHandler(ch)
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.fatal("test")
        return ch

    def test_debug(self):
        ch = self.log(4)
        self.assertEqual(len(ch.buffer), 4)

    def test_info(self):
        ch = self.log(3)
        self.assertEqual(len(ch.buffer), 3)

    def test_warn(self):
        ch = self.log(2)
        self.assertEqual(len(ch.buffer), 2)

    def test_fatal(self):
        ch = self.log(1)
        self.assertEqual(len(ch.buffer), 1)


if __name__ == "__main__":
    unittest.main()
