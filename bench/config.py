#  Copyright (c) 2024, Xeraph
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree.

import os
import tomllib
from dataclasses import dataclass
from typing import Any

from .colors import blue, cyan, green, yellow


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
    no_build: bool

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data["name"]
        self.cmd_path = data["cmd"]
        self.build = data["build"] if "build" in data else ""
        self.simple_build = data["simple_build"] if "simple_build" in data else False
        self.no_build = data["no_build"] if "no_build" in data else False

    def cmd(self, challenge: str, developer: str) -> list[str]:
        split = self.cmd_path.split(" ")
        command = split[0]
        path = " ".join(split[1:]) if len(split) > 1 else self.cmd_path
        path = path.replace(":challenge", challenge)
        path = path.replace(":developer", developer)
        cmd = []
        if self.no_build:
            cmd.append(command)
        cmd.append(path)
        return cmd

    def build_cmd(self, challenge: str, developer: str) -> list[str]:
        cmd = self.build.replace(":challenge", challenge)
        cmd = cmd.replace(":developer", developer)
        return [cmd.split(" ")[0]] + cmd.split(" ")[1:]


class ChallengeDeveloperName(str):
    def __format__(self, format_spec: str) -> str:
        return blue(self)


@dataclass
class ChallengeDeveloper:
    username: ChallengeDeveloperName
    languages: list[str]

    def __init__(self, data: dict[str, Any]) -> None:
        self.username = ChallengeDeveloperName(data["username"])
        self.languages = data["languages"]
        self.languages.sort()

    def __format__(self, format_spec: str) -> str:
        return f"{self.username}"


class ChallengeLanguageName(str):
    def __format__(self, format_spec: str) -> str:
        return cyan(self)


@dataclass
class ChallengeLanguage:
    name: ChallengeLanguageName

    def __init__(self, name: str) -> None:
        self.name = ChallengeLanguageName(name)

    def __format__(self, format_spec: str) -> str:
        return f"{self.name}"


class ChallengeLevelName(str):
    def __format__(self, format_spec: str) -> str:
        return yellow(self)


@dataclass
class ChallengeLevel:
    name: ChallengeLevelName
    input: list[str]
    output: str

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = ChallengeLevelName(data["name"])
        self.input = data["input"]
        self.output = data["output"]

    def __format__(self, format_spec: str) -> str:
        return f"{self.name}"


class ChallengeName(str):
    def __format__(self, format_spec: str) -> str:
        return green(self)


@dataclass
class Challenge:
    key: ChallengeName
    name: ChallengeName
    levels: list[ChallengeLevel]
    developers: list[ChallengeDeveloper]
    languages: list[ChallengeLanguage]

    def __init__(self, data: dict[str, Any]) -> None:
        self.key = ChallengeName(data["key"])
        self.name = ChallengeName(data["name"])
        self.levels = []
        self.developers = []
        self.languages = []

    def withLevels(self, levels: list[ChallengeLevel]):
        self.levels = levels
        return self

    def withDevelopers(self, developers: list[ChallengeDeveloper]):
        self.developers = developers
        return self

    def withLanguages(self, languages: list[ChallengeLanguage]):
        self.languages = languages
        return self

    def __format__(self, format_spec: str) -> str:
        value = self.name if format_spec == "name" else self.key
        return f"{value}"


class Config:
    path: str
    general: General
    developers: dict[str, Developer]
    languages: dict[str, Language]
    challenges: dict[str, Challenge]
    data: dict[str, Any]

    def __init__(self) -> None:
        self.path = os.path.join(os.getcwd(), "bench.toml")

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
                    challenge_language = ChallengeLanguage(language)
                    if challenge_language not in ch.languages:
                        ch.languages.append(challenge_language)

            ch.developers.sort(key=lambda dev: dev.username)
            ch.languages.sort(key=lambda lang: lang.name)

    def load(self) -> None:
        with open(self.path, mode="rb") as fp:
            self.data = tomllib.load(fp)
