# Languages Benchmarks

> [!IMPORTANT]
> - Don't cheat, create a real algorithm that solves the requested problem.
> - Use all the resources provided by the language and its std, even concurrency and/or multithreading.
> - FFI is not allowed, use the language itself.
> - Compute the answer by brute force, don't do divide and conquer, but is allowed to split the algorithm by chunks (useful when threading).

> [!NOTE]
> To add another language, create a new folder and branch with the language name. If the name has any symbols like C#, use another name like csharp.

> Structure your subproject to have one executable file per challenge. Example:
>
> ```shell
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
>
> - the first, a string representing the secret key
> - the second, an integer between 5 and 7 representing the number of zeros
>
> Try locally with the inputs provided on the challenge page
>
> Just compute the requested number and print it

### 5 zeros

| Command            |   Mean [ms] | Min [ms] | Max [ms] |     Relative |
| :----------------- | ----------: | -------: | -------: | -----------: |
| `bench-zig`        |   8.6 ± 0.8 |      7.6 |     10.1 |         1.00 |
| `bench-rust`       |  10.1 ± 0.9 |      9.0 |     12.0 |  1.18 ± 0.14 |
| `bench-go`         |  13.1 ± 0.6 |     12.2 |     13.9 |  1.52 ± 0.15 |
| `bench-haskell`    |  76.8 ± 8.9 |     64.3 |     87.7 |  8.93 ± 1.30 |
| `bench-php`        |  77.0 ± 0.3 |     76.4 |     77.6 |  8.95 ± 0.80 |
| `bench-swift`      |  82.6 ± 1.9 |     80.6 |     87.6 |  9.60 ± 0.88 |
| `bench-javascript` | 101.6 ± 1.0 |    100.1 |    103.1 | 11.81 ± 1.06 |
| `bench-python`     | 275.3 ± 5.6 |    270.0 |    284.6 | 32.01 ± 2.92 |

### 6 zeros

| Command            |      Mean [ms] | Min [ms] | Max [ms] |     Relative |
| :----------------- | -------------: | -------: | -------: | -----------: |
| `bench-zig`        |    171.8 ± 4.5 |    164.2 |    177.7 |         1.00 |
| `bench-rust`       |    212.5 ± 9.3 |    200.0 |    231.3 |  1.24 ± 0.06 |
| `bench-go`         |   306.1 ± 14.8 |    292.2 |    343.8 |  1.78 ± 0.10 |
| `bench-php`        |   1887.9 ± 4.6 |   1880.0 |   1898.6 | 10.99 ± 0.29 |
| `bench-haskell`    | 2055.6 ± 174.3 |   1770.9 |   2263.2 | 11.96 ± 1.06 |
| `bench-swift`      |  2482.1 ± 70.2 |   2393.1 |   2597.0 | 14.44 ± 0.56 |
| `bench-python`     |  2989.5 ± 79.0 |   2880.4 |   3102.5 | 17.40 ± 0.65 |
| `bench-javascript` |  3060.2 ± 15.2 |   3035.6 |   3075.7 | 17.81 ± 0.48 |

### 7 zeros

| Command            |       Mean [s] | Min [s] | Max [s] |     Relative |
| :----------------- | -------------: | ------: | ------: | -----------: |
| `bench-zig`        |  1.102 ± 0.061 |   1.041 |   1.213 |         1.00 |
| `bench-rust`       |  1.294 ± 0.022 |   1.263 |   1.346 |  1.17 ± 0.07 |
| `bench-go`         |  1.805 ± 0.014 |   1.779 |   1.822 |  1.64 ± 0.09 |
| `bench-php`        | 10.535 ± 0.050 |  10.487 |  10.657 |  9.56 ± 0.53 |
| `bench-swift`      | 15.206 ± 0.121 |  15.004 |  15.392 | 13.79 ± 0.77 |
| `bench-haskell`    | 15.328 ± 1.067 |  12.489 |  16.290 | 13.90 ± 1.24 |
| `bench-python`     | 17.261 ± 1.014 |  15.568 |  18.186 | 15.66 ± 1.27 |
| `bench-javascript` | 17.468 ± 0.151 |  17.250 |  17.843 | 15.85 ± 0.89 |

## [Advent of Code - Year 2020 - Day 15](https://adventofcode.com/2020/day/15)

> [!IMPORTANT]
> The program must accept positional arguments in the below way
>
> - the first, an integer representing nth number spoken to determine
> - the rest, a list of integers representing the starting numbers
>
> Try locally with the inputs provided on the challenge page
>
> Just compute the requested number and print it

### 30000000th number spoken

| Command       |   Mean [ms] | Min [ms] | Max [ms] |    Relative |
| :------------ | ----------: | -------: | -------: | ----------: |
| `bench-swift` | 745.5 ± 3.8 |    741.3 |    753.6 |        1.00 |
| `bench-go`    | 805.9 ± 2.0 |    802.8 |    808.3 | 1.08 ± 0.01 |
