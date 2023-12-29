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
| `bench-javascript` | 97.9 ± 0.9 | 96.7 | 100.0 | 8.10 ± 0.67 |
| `bench-go` | 12.1 ± 1.0 | 10.9 | 13.8 | 1.00 |
| `bench-python` | 253.1 ± 7.0 | 238.6 | 261.0 | 20.94 ± 1.81 |
| `bench-swift` | 160.4 ± 1.3 | 159.0 | 163.4 | 13.27 ± 1.09 |

### 6 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 3.026 ± 0.030 | 2.993 | 3.104 | 11.49 ± 0.28 |
| `bench-go` | 0.263 ± 0.006 | 0.257 | 0.272 | 1.00 |
| `bench-python` | 2.926 ± 0.058 | 2.818 | 2.987 | 11.11 ± 0.33 |
| `bench-swift` | 5.495 ± 0.023 | 5.443 | 5.521 | 20.87 ± 0.48 |

### 7 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 17.393 ± 0.323 | 17.089 | 18.187 | 11.46 ± 0.27 |
| `bench-go` | 1.517 ± 0.021 | 1.495 | 1.569 | 1.00 |
| `bench-python` | 15.750 ± 0.602 | 14.886 | 16.476 | 10.38 ± 0.42 |
