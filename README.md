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
  Time (mean ± σ):     537.6 ms ±   3.5 ms    [User: 2609.2 ms, System: 138.6 ms]
  Range (min … max):   533.0 ms … 542.0 ms    10 runs

Benchmark 2: swift/.build/release/aoc-year2015-day4
  Time (mean ± σ):     11.609 s ±  0.487 s    [User: 11.502 s, System: 0.009 s]
  Range (min … max):   11.239 s … 12.843 s    10 runs

Summary
  go/build/aoc-year2015-day4 ran
   21.59 ± 0.92 times faster than swift/.build/release/aoc-year2015-day4
```
