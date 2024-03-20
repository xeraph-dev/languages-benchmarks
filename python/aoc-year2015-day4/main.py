## WARNING: Python 3.12 only
import os
import sys
from threading import Thread
import _xxsubinterpreters as interpreters
import _xxinterpchannels as channels

worker_payload = """
from hashlib import md5
import _xxinterpchannels as channels
compare_zeroes = "0" * zeroes
prehash = md5(prefix.encode())
for i in range(start, end):
    hash = prehash.copy()
    hash.update(str(i).encode())
    if hash.hexdigest().startswith(compare_zeroes):
        channels.send(channel, i)
        break
"""


def compute(prefix: str, zeroes: int, workers_count):
    workers = [interpreters.create() for x in range(workers_count)]
    batch_size = 2**16
    channel = channels.create()

    solutions = []

    start = 0
    while True:
        threads = []
        for worker in workers:
            worker_arguments = {
                "script": worker_payload,
                "id": worker,
                "shared": {
                    "channel": channel,
                    "prefix": prefix,
                    "zeroes": zeroes,
                    "start": start,
                    "end": start + batch_size,
                },
            }
            t = Thread(target=interpreters.run_string, kwargs=worker_arguments)
            t.start()
            threads.append(t)
            start += batch_size

        for thread in threads:
            thread.join()

        for _ in range(workers_count):
            if (possible_solution := channels.recv(channel, None)) != None:
                solutions.append(possible_solution)

        if solutions:
            [interpreters.destroy(worker) for worker in workers]
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

    print(compute(prefix, zeroes, os.cpu_count()))
    exit(0)
