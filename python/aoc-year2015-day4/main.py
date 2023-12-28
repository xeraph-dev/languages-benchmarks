## WARNING: Python 3.12 only
import os
import sys
from threading import Thread
from time import sleep
import _xxsubinterpreters as interpreters
import _xxinterpchannels as channels

WORKERS = [interpreters.create() for x in range(os.cpu_count())]
CHUNK_SIZE = 2**16

worker_payload = """
# Needs (channel: int, prefix: str, zeroes: int, start: int, end: int):
from hashlib import md5
import _xxinterpchannels as channels
compare_zeroes: str = "0" * zeroes
prehash = md5(prefix.encode())
for i in range(start, end):
    hash = prehash.copy()
    hash.update(str(i).encode())
    if hash.hexdigest().startswith(compare_zeroes):
        channels.send(channel, i)
        break
channels.send(channel, None)
"""


def compute(prefix: str, zeroes: int):
    channel = channels.create()

    start = 0
    solutions = []

    while True:
        for worker in WORKERS:
            worker_arguments = {
                "script": worker_payload,
                "id": worker,
                "shared": {
                    "channel": channel,
                    "prefix": prefix,
                    "zeroes": zeroes,
                    "start": start,
                    "end": start + CHUNK_SIZE,
                },
            }
            Thread(target=interpreters.run_string, kwargs=worker_arguments).start()
            start += CHUNK_SIZE

        for worker in WORKERS:
            while interpreters.is_running(worker):
                sleep(0.0001)

        for worker in WORKERS:
            try:
                possible_solution = channels.recv(channel)
                if possible_solution != None:
                    solutions.append(possible_solution)
            except Exception as e:
                pass

        if solutions:
            return min(solutions)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Parameters: secret zeroes")
        os._exit(1)

    prefix = sys.argv[1]

    try:
        zeroes = int(sys.argv[2])
        if zeroes < 0 or zeroes > 32:
            raise Exception()
    except:
        print("Zeroes should be an integer between 0-32")
        os._exit(1)

    print(compute(prefix=prefix, zeroes=zeroes))
    os._exit(0)