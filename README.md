# Languages Benchmarks

> [!IMPORTANT]
> Don't cheat, create a real algorithm that solves the requested problem.

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
  Time (mean ± σ):     537.9 ms ±   4.3 ms    [User: 2610.6 ms, System: 138.0 ms]
  Range (min … max):   532.4 ms … 544.0 ms    10 runs

Benchmark 2:  rust/target/release/aoc-year2015-day4
  Time (mean ± σ):     622.5 ms ±  68.9 ms    [User: 3142.6 ms, System: 331.5 ms]
  Range (min … max):   549.1 ms … 699.5 ms    10 runs

Benchmark 3:  swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):     11.159 s ±  0.058 s    [User: 11.088 s, System: 0.003 s]
  Range (min … max):   11.083 s … 11.266 s    10 runs

Summary
   go/build/aoc-year2015-day4 ran
    1.16 ± 0.13 times faster than  rust/target/release/aoc-year2015-day4
   20.74 ± 0.20 times faster than  swift/.build/release/aoc-year2015-day4
```
