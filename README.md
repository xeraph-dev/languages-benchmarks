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
hyperfine --warmup 1 go/build/aoc-year2015-day4 'python python/aoc-year2015-day4/main.py' rust/target/release/aoc-year2015-day4 swift/.build/release/aoc-year2015-day4
```

```shell
Benchmark 1:  go/build/aoc-year2015-day4
  Time (mean ± σ):     576.4 ms ±  15.6 ms    [User: 3225.7 ms, System: 133.0 ms]
  Range (min … max):   555.1 ms … 603.1 ms    10 runs

Benchmark 2:  python python/aoc-year2015-day4/main.py
  Time (mean ± σ):      4.444 s ±  0.164 s    [User: 31.905 s, System: 0.138 s]
  Range (min … max):    4.215 s …  4.659 s    10 runs

Benchmark 3:  rust/target/release/aoc-year2015-day4
  Time (mean ± σ):     752.5 ms ±  95.4 ms    [User: 3413.0 ms, System: 370.7 ms]
  Range (min … max):   577.2 ms … 861.8 ms    10 runs

Benchmark 4:  swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):      9.182 s ±  0.051 s    [User: 9.103 s, System: 0.007 s]
  Range (min … max):    9.114 s …  9.291 s    10 runs

Summary
   go/build/aoc-year2015-day4 ran
    1.31 ± 0.17 times faster than  rust/target/release/aoc-year2015-day4
    7.71 ± 0.35 times faster than  python python/aoc-year2015-day4/main.py
   15.93 ± 0.44 times faster than  swift/.build/release/aoc-year2015-day4
```
