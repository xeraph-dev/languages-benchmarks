import unittest

from bench.tests.utils import (
    load_config,
    mock_challenges,
    mock_developers,
    mock_general,
    mock_languages,
)


class TestConfig(unittest.TestCase):
    def test_init(self) -> None:
        config = load_config()

        self.assertEqual(config.general, mock_general)
        self.assertEqual(config.developers, mock_developers)
        self.assertEqual(config.languages, mock_languages)
        self.assertEqual(config.challenges, mock_challenges)


if __name__ == "__main__":
    unittest.main()
