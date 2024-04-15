from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib


@dataclass
class General:
    runs: int
    warmups: int
    timeout: int
    max_timeouts: int

    def __init__(self, data: dict[str, Any]) -> None:
        self.runs = data["runs"]
        self.warmups = data["warmups"]
        self.timeout = data["timeout"]
        self.max_timeouts = data["max_timeouts"]


@dataclass
class Developer:
    username: str

    def __init__(self, data: dict[str, Any]) -> None:
        self.username = data["username"]


@dataclass
class Language:
    name: str
    cmd_path: str
    build: str
    simple_build: bool

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data["name"]
        self.cmd_path = data["cmd"]
        self.build = data["build"]
        self.simple_build = data["simple_build"]

    def cmd(self, challenge: str, developer: str) -> Path:
        path = self.cmd_path.replace(":challenge", challenge)
        path = path.replace(":developer", developer)
        return Path(path)

    def build_cmd(self, challenge: str, developer: str) -> list[str]:
        cmd = self.build.replace(":challenge", challenge)
        cmd = cmd.replace(":developer", developer)
        return [cmd.split(" ")[0]] + cmd.split(" ")[1:]


@dataclass
class ChallengeDeveloper:
    username: str
    languages: list[str]

    def __init__(self, data: dict[str, Any]) -> None:
        self.username = data["username"]
        self.languages = data["languages"]
        self.languages.sort()


@dataclass
class ChallengeLevel:
    name: str
    input: list[str]
    output: str

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data["name"]
        self.input = data["input"]
        self.output = data["output"]


@dataclass
class Challenge:
    key: str
    name: str
    levels: list[ChallengeLevel]
    developers: list[ChallengeDeveloper]
    languages: list[str]

    def __init__(self, data: dict[str, Any]) -> None:
        self.key = data["key"]
        self.name = data["name"]
        self.levels = []
        self.developers = []
        self.languages = []

    def withLevels(self, levels: list[ChallengeLevel]):
        self.levels = levels
        return self

    def withDevelopers(self, developers: list[ChallengeDeveloper]):
        self.developers = developers
        return self

    def withLanguages(self, languages: list[str]):
        self.languages = languages
        return self


class Config:
    path: str
    general: General
    developers: dict[str, Developer]
    languages: dict[str, Language]
    challenges: dict[str, Challenge]
    data: dict[str, Any]

    def __init__(self, path: str) -> None:
        self.path = path

        self.load()

        self.developers = {}
        self.languages = {}
        self.challenges = {}

        self.general = General(self.data["general"])

        for developer in self.data["developers"]:
            self.developers[developer["username"]] = Developer(developer)

        for language in self.data["languages"]:
            self.languages[language["name"]] = Language(language)

        for challenge in self.data["challenges"]:
            self.challenges[challenge["key"]] = ch = Challenge(challenge)

            for level in challenge["levels"]:
                ch.levels.append(ChallengeLevel(level))

            for developer in challenge["developers"]:
                ch.developers.append(ChallengeDeveloper(developer))
                for language in developer["languages"]:
                    if language not in ch.languages:
                        ch.languages.append(language)

            ch.developers.sort(key=lambda dev: dev.username)
            ch.languages.sort()

    def load(self) -> None:
        with open(self.path, mode="rb") as fp:
            self.data = tomllib.load(fp)
