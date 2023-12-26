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

## [Advent of Code - Year 2015 - Day 4 - part 2](https://adventofcode.com/2015/day/4#part2)

> [!IMPORTANT]
> input: `yzbqklnj`
>
> Remember, part 2, six zeros, not five.

Just compute the requested number and print it.

```shell
hyperfine --warmup 1 go/build/aoc-year2015-day4 'php php/aoc-year2015-day4/main.php' 'python python/aoc-year2015-day4/main.py' rust/target/release/aoc-year2015-day4 swift/.build/release/aoc-year2015-day4
```

```shell
Benchmark 1:  go/build/aoc-year2015-day4
  Time (mean ± σ):     641.1 ms ±  13.3 ms    [User: 3277.2 ms, System: 144.6 ms]
  Range (min … max):   627.3 ms … 673.0 ms    10 runs

Benchmark 2:  php php/aoc-year2015-day4/main.php
  Time (mean ± σ):      3.512 s ±  0.022 s    [User: 3.461 s, System: 0.014 s]
  Range (min … max):    3.495 s …  3.570 s    10 runs

Benchmark 3:  python python/aoc-year2015-day4/main.py
  Time (mean ± σ):      4.922 s ±  0.156 s    [User: 33.330 s, System: 0.183 s]
  Range (min … max):    4.596 s …  5.140 s    10 runs

Benchmark 4:  rust/target/release/aoc-year2015-day4
  Time (mean ± σ):     753.0 ms ±  59.0 ms    [User: 3417.4 ms, System: 367.8 ms]
  Range (min … max):   610.9 ms … 812.3 ms    10 runs

Benchmark 5:  swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):      9.179 s ±  0.044 s    [User: 9.105 s, System: 0.005 s]
  Range (min … max):    9.101 s …  9.237 s    10 runs

Summary
   go/build/aoc-year2015-day4 ran
    1.17 ± 0.10 times faster than  rust/target/release/aoc-year2015-day4
    5.48 ± 0.12 times faster than  php php/aoc-year2015-day4/main.php
    7.68 ± 0.29 times faster than  python python/aoc-year2015-day4/main.py
   14.32 ± 0.31 times faster than  swift/.build/release/aoc-year2015-day4
```
