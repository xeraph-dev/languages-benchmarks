import resource
import time
from dataclasses import dataclass
from logging import Logger
from subprocess import TimeoutExpired

from bench.config import Challenge, ChallengeDeveloper, ChallengeLevel, Config, Language


@dataclass
class BenchmarkMeasure:
    time: str
    ram: str
    cpu: str


@dataclass
class BenchmarkStats:
    challenge: str
    level: str
    language: str
    developer: str
    times: list[BenchmarkMeasure]
    rams: list[BenchmarkMeasure]
    successes: int
    fails: int
    timeouts: int

    def __init__(
        self,
        challenge: Challenge,
        level: ChallengeLevel,
        language: Language,
        developer: ChallengeDeveloper,
    ) -> None:
        self.challenge = challenge.name
        self.level = level.name
        self.language = language.name
        self.developer = developer.username

        self.times = []
        self.rams = []

        self.successes = 0
        self.fails = 0
        self.timeouts = 0


def benchmark(
    logger: Logger, config: Config, challenges: list[Challenge]
) -> list[BenchmarkStats]:
    stats = list[BenchmarkStats]()

    for challenge in challenges:
        for level in challenge.levels:
            for developer in challenge.developers:
                for language in developer.languages:
                    language = config.languages[language]

                    cmd = language.cmd(challenge.key, developer.username)
                    if not cmd.exists():
                        logger.warning(f"Missing file {cmd}, skipping")
                        continue

                    for i in range(config.general.warmups + config.general.runs):
                        stat = BenchmarkStats(challenge, level, language, developer)
                        stats.append(stat)

                        try:
                            start = time.time_ns()

                            end = time.time_ns()

                            rss = resourcece.getrusage(
                                resource.RUSAGE_CHILDREN
                            ).ru_maxrss
                        except TimeoutExpired:
                            if i < config.general.warmups:
                                continue
                            stat.timeouts += 1

    return stats


#                     for i in range(self.config.warmups + self.config.runs):
#                         try:
#                             start = time.time_ns()

#                             proc = subprocess.Popen(
#                                 cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#                             )
#                             proc.wait(self.config.timeout)

#                             end = time.time_ns() - start
#                             rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
#                             if proc.stdout:
#                                 output = proc.stdout.read().strip().decode("utf-8")

#                             if i < self.config.warmups:
#                                 continue
#                             if proc.returncode == 0 and output == level.output:
#                                 stat.success += 1
#                                 stat.time.append(end)
#                                 stat.ram.append(rss)
#                             else:
#                                 stat.fail += 1
#                         except subprocess.TimeoutExpired:
#                             if i < self.config.warmups:
#                                 continue
#                             stat.timeout += 1

#     def print(self) -> None:
#         print(self.stats)
