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
| `bench-go` | 15.7 ± 1.0 | 14.6 | 18.0 | 1.00 |
| `bench-python` | 366.0 ± 5.4 | 355.9 | 373.7 | 23.26 ± 1.50 |
| `bench-swift` | 242.9 ± 1.3 | 241.2 | 244.7 | 15.43 ± 0.97 |

### 6 zeros

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `bench-go` | 504.5 ± 42.0 | 440.1 | 583.1 | 1.00 |
| `bench-python` | 4735.1 ± 225.0 | 4476.2 | 5053.7 | 9.38 ± 0.90 |
| `bench-swift` | 8351.2 ± 54.1 | 8301.5 | 8444.8 | 16.55 ± 1.38 |

### 7 zeros

|| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-go` | 2.565 ± 0.025 | 2.519 | 2.602 | 1.00 |
| `bench-python` | 24.881 ± 1.511 | 23.551 | 28.918 | 9.70 ± 0.60 |
