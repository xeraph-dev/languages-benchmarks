import tempfile

from bench.config import (
    Challenge,
    ChallengeDeveloper,
    ChallengeLevel,
    Config,
    Developer,
    General,
    Language,
)

mock_general = General({"runs": 2, "warmups": 1, "timeout": 30, "max_timeouts": 3})

mock_developers = {
    "developer-1": Developer({"username": "developer-1"}),
    "developer-2": Developer({"username": "developer-2"}),
}

mock_languages = {
    "go": Language(
        {"name": "go", "cmd": "golang cmd path", "build": "golang build command"}
    ),
    "swift": Language(
        {"name": "swift", "cmd": "swift cmd path", "build": "swift build command"}
    ),
}

mock_challenges = {
    "challenge-1": Challenge({"key": "challenge-1", "name": "Challenge 1"})
    .withLevels(
        [
            ChallengeLevel(
                {"name": "secret 1", "input": ["secret-1", "5"], "output": "output-1"}
            ),
            ChallengeLevel(
                {"name": "secret 2", "input": ["secret-2", "6"], "output": "output-2"}
            ),
            ChallengeLevel(
                {"name": "secret 3", "input": ["secret-3", "7"], "output": "output-3"}
            ),
        ]
    )
    .withDevelopers(
        [
            ChallengeDeveloper({"username": "developer-1", "languages": ["swift"]}),
            ChallengeDeveloper({"username": "developer-2", "languages": ["go"]}),
        ]
    )
    .withLanguages(["go", "swift"]),
    "challenge-2": Challenge(
        {
            "key": "challenge-2",
            "name": "Challenge 2",
        }
    )
    .withLevels(
        [
            ChallengeLevel(
                {"name": "secret 1", "input": ["secret-1", "10"], "output": "output-1"}
            ),
        ]
    )
    .withDevelopers(
        [
            ChallengeDeveloper({"username": "developer-1", "languages": ["swift"]}),
            ChallengeDeveloper({"username": "developer-2", "languages": ["go"]}),
        ]
    )
    .withLanguages(["go", "swift"]),
}


def load_config() -> Config:
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        fp.write(b"""
[general]
runs = 2
warmups = 1
timeout = 30
max_timeouts = 3


[[developers]]
username = "developer-1"

[[developers]]
username = "developer-2"


[[languages]]
name = "go"
cmd = "golang cmd path"
build = "golang build command"

[[languages]]
name = "swift"
cmd = "swift cmd path"
build = "swift build command"


[[challenges]]
key = "challenge-1"
name = "Challenge 1"
[[challenges.levels]]
name = "secret 1"
input = ["secret-1", "5"]
output = "output-1"
[[challenges.levels]]
name = "secret 2"
input = ["secret-2", "6"]
output = "output-2"
[[challenges.levels]]
name = "secret 3"
input = ["secret-3", "7"]
output = "output-3"
[[challenges.developers]]
username = "developer-1"
languages = ["swift"]
[[challenges.developers]]
username = "developer-2"
languages = ["go"]

[[challenges]]
key = "challenge-2"
name = "Challenge 2"
[[challenges.levels]]
name = "secret 1"
input = ["secret-1", "10"]
output = "output-1"
[[challenges.developers]]
username = "developer-1"
languages = ["swift"]
[[challenges.developers]]
username = "developer-2"
languages = ["go"]
""")
        fp.close()
        return Config(fp.name)
