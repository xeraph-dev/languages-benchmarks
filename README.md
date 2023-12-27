# Languages Benchmarks

> [!IMPORTANT]
> - Don't cheat, create a real algorithm that solves the requested problem.
> - Use all the resources provided by the language and its std, even concurrency and/or multithreading.
> - FFI is not allowed, use the language itself.
> - Compute the answer by brute force, don't do divide and conquer, but is allowed to split the algorithm by chunks (useful when threading).
> - Don't do public the answer, do first the oficial challenge with your inputs, and then change to the inputs provided by this readme.

> [!NOTE]
> To add another language, create a new folder and branch with the language name. If the name has any symbols like C#, use another name like csharp.

> Structure your subproject to have one executable file per challenge. Example:
> ```
> language/
>   challenge-1/
>     main.lang
>   challenge-2/
>     main.lang
> ```

## Tools used

- Benchmark: [hyperfine](https://github.com/sharkdp/hyperfine)
- Task runner: [task](https://taskfile.dev/)

## [Advent of Code - Year 2015 - Day 4](https://adventofcode.com/2015/day/4)

> [!IMPORTANT]
> The program must accept two positional arguments
> - the first, a string representing the secret key
> - the second, an integer between 5 and 7 representing the number of zeros
>
> Try locally with the inputs provided on the challenge page
>
> Just compute the requested number and print it

### Old benchmarks

```shell
hyperfine --warmup 1 \
  go/build/aoc-year2015-day4 \
  'php php/aoc-year2015-day4/main.php' \
  'python python/aoc-year2015-day4/main.py' \
  rust/target/release/aoc-year2015-day4 \
  swift/.build/release/aoc-year2015-day4 \
  zig/zig-out/bin/aoc-year2015-day4
```

<section class="tabs">
  <details open>
    <summary>summary</summary>

    Summary
      go/build/aoc-year2015-day4 ran
        1.27 ± 0.10 times faster than  rust/target/release/aoc-year2015-day4
        6.21 ± 0.11 times faster than  php php/aoc-year2015-day4/main.php
        8.54 ± 0.33 times faster than  python python/aoc-year2015-day4/main.py
       16.23 ± 0.32 times faster than  swift/.build/release/aoc-year2015-day4
       26.01 ± 0.49 times faster than  zig/zig-out/bin/aoc-year2015-day4
  </details>
  <details>
    <summary>go</summary>

    Benchmark 1:  go/build/aoc-year2015-day4
      Time (mean ± σ):     564.3 ms ±  10.3 ms    [User: 3170.9 ms, System: 135.1 ms]
      Range (min … max):   551.5 ms … 583.0 ms    10 runs
  </details>
  <details>
    <summary>php</summary>

    Benchmark 2:  php php/aoc-year2015-day4/main.php
      Time (mean ± σ):      3.502 s ±  0.007 s    [User: 3.462 s, System: 0.011 s]
      Range (min … max):    3.494 s …  3.515 s    10 runs
  </details>
  <details>
    <summary>python</summary>

    Benchmark 3:  python python/aoc-year2015-day4/main.py
      Time (mean ± σ):      4.822 s ±  0.163 s    [User: 32.297 s, System: 0.171 s]
      Range (min … max):    4.543 s …  5.006 s    10 runs
  </details>
  <details>
    <summary>rust</summary>

    Benchmark 4:  rust/target/release/aoc-year2015-day4
      Time (mean ± σ):     716.5 ms ±  52.8 ms    [User: 3398.3 ms, System: 375.2 ms]
      Range (min … max):   595.8 ms … 799.2 ms    10 runs
  </details>
  <details>
    <summary>swift</summary>

    Benchmark 5:  swift/.build/release/aoc-year2015-day4
      Time (mean ± σ):      9.159 s ±  0.070 s    [User: 9.087 s, System: 0.004 s]
      Range (min … max):    9.062 s …  9.242 s    10 runs
  </details>
  <details>
    <summary>zig</summary>

    Benchmark 6:  zig/zig-out/bin/aoc-year2015-day4
      Time (mean ± σ):     14.675 s ±  0.074 s    [User: 14.542 s, System: 0.032 s]
      Range (min … max):   14.563 s … 14.825 s    10 runs
  </details>
</section>
