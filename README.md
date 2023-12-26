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
hyperfine --warmup 1 go/build/aoc-year2015-day4 rust/target/release/aoc-year2015-day4 swift/.build/release/aoc-year2015-day4
```

```shell
Benchmark 1:  go/build/aoc-year2015-day4
  Time (mean ± σ):     597.4 ms ±  28.1 ms    [User: 3233.3 ms, System: 138.6 ms]
  Range (min … max):   576.4 ms … 660.6 ms    10 runs

Benchmark 2:  rust/target/release/aoc-year2015-day4
  Time (mean ± σ):     777.8 ms ±  43.9 ms    [User: 3494.0 ms, System: 387.3 ms]
  Range (min … max):   720.8 ms … 881.2 ms    10 runs

Benchmark 3:  swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):      9.125 s ±  0.074 s    [User: 9.069 s, System: 0.003 s]
  Range (min … max):    9.018 s …  9.231 s    10 runs

Summary
   go/build/aoc-year2015-day4 ran
    1.30 ± 0.10 times faster than  rust/target/release/aoc-year2015-day4
   15.28 ± 0.73 times faster than  swift/.build/release/aoc-year2015-day4
```
