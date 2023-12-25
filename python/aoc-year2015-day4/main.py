## WARNING: Python 3.12 only
from threading import Thread
import _xxsubinterpreters as interpreters
import _xxinterpchannels as channels


WORKERS = [interpreters.create() for x in range(8)]
CHUNK_SIZE = 10000

channel = channels.create()

worker_payload = """
# Needs (channel: int, prefix: str, zeroes: int, start: int, end: int):
from hashlib import md5
import _xxinterpchannels as channels
compare_zeroes: str = "0" * zeroes
prehash = md5(prefix.encode())
numbers_set = set(range(start, end))
for i in number_set:
    hash = prehash.copy()
    hash.update(str(i).encode())
    if hash.hexdigest()[zeroes:] == compare_zeroes):
        channels.send(channel, i)
        break
channels.send(channel, None)
"""


def compute(prefix: str, zeroes: int):
    start = 0
    solutions = []

    while True:
        for worker in WORKERS:
            while interpreters.is_running(worker):
                pass
            Thread(
                target=interpreters.run_string,
                kwargs={
                    "script": worker_payload,
                    "id": worker,
                    "shared": {
                        "channel": channel,
                        "prefix": prefix,
                        "zeroes": zeroes,
                        "start": start,
                        "end": start + CHUNK_SIZE,
                    },
                },
            ).start()
            start += CHUNK_SIZE

        for i in range(len(WORKERS) + 1):
            try:
                possible_solution = channels.recv(channel)
                if possible_solution != None:
                    solutions.append(possible_solution)
            except:
                if solutions:
                    return min(solutions)
                else:
                    break


print("Result:", compute(prefix="yzbqklnj", zeroes=6))
