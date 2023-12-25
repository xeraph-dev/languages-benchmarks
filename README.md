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
hyperfine --warmup 1 go/build/aoc-year2015-day4 swift/.build/release/aoc-year2015-day4
```

```shell
Benchmark 1: go/build/aoc-year2015-day4
  Time (mean ± σ):     573.2 ms ±  25.1 ms    [User: 3114.6 ms, System: 137.4 ms]
  Range (min … max):   538.3 ms … 621.0 ms    10 runs

Benchmark 2: swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):      9.041 s ±  0.060 s    [User: 8.993 s, System: 0.004 s]
  Range (min … max):    8.965 s …  9.147 s    10 runs

Summary
  go/build/aoc-year2015-day4 ran
   15.77 ± 0.70 times faster than swift/.build/release/aoc-year2015-day4
```
