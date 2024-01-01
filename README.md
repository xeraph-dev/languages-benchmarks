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

### 5 zeros

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `bench-rust` | 14.4 ± 1.4 | 12.7 | 17.2 | 1.04 ± 0.11 |
| `bench-javascript` | 99.7 ± 0.6 | 98.7 | 100.6 | 7.20 ± 0.25 |
| `bench-go` | 13.8 ± 0.5 | 12.9 | 14.5 | 1.00 |
| `bench-python` | 257.3 ± 2.8 | 253.4 | 262.4 | 18.59 ± 0.67 |
| `bench-swift` | 80.0 ± 1.9 | 76.0 | 82.5 | 5.78 ± 0.24 |
| `bench-haskell` | 74.4 ± 5.8 | 64.7 | 79.3 | 5.37 ± 0.46 |

### 6 zeros

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `bench-rust` | 303.3 ± 6.0 | 295.9 | 312.3 | 1.00 |
| `bench-javascript` | 3277.5 ± 295.5 | 3037.1 | 3811.2 | 10.81 ± 1.00 |
| `bench-go` | 310.9 ± 7.2 | 301.7 | 320.4 | 1.03 ± 0.03 |
| `bench-python` | 2940.5 ± 79.4 | 2841.8 | 3065.6 | 9.70 ± 0.32 |
| `bench-swift` | 2193.9 ± 774.1 | 15.1 | 2606.5 | 7.23 ± 2.56 |
| `bench-haskell` | 2293.8 ± 266.6 | 1936.2 | 2841.3 | 7.56 ± 0.89 |

### 7 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-rust` | 2.854 ± 0.500 | 2.286 | 3.967 | 1.49 ± 0.36 |
| `bench-javascript` | 17.334 ± 0.171 | 17.125 | 17.629 | 9.07 ± 1.49 |
| `bench-go` | 1.912 ± 0.313 | 1.748 | 2.773 | 1.00 |
| `bench-python` | 15.761 ± 0.413 | 15.037 | 16.273 | 8.25 ± 1.37 |
| `bench-swift` | 15.743 ± 0.580 | 15.006 | 16.593 | 8.24 ± 1.38 |
| `bench-haskell` | 14.061 ± 1.588 | 11.572 | 16.872 | 7.36 ± 1.46 |
