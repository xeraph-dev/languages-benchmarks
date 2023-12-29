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
| `bench-go` | 12.0 ± 0.4 | 11.5 | 13.1 | 1.00 |
| `bench-python` | 252.0 ± 4.5 | 247.1 | 261.6 | 21.07 ± 0.87 |
| `bench-swift` | 156.2 ± 0.7 | 155.3 | 157.0 | 13.05 ± 0.49 |

### 6 zeros

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `bench-go` | 269.6 ± 8.2 | 260.6 | 283.2 | 1.00 |
| `bench-python` | 2983.0 ± 92.1 | 2817.3 | 3100.3 | 11.07 ± 0.48 |
| `bench-swift` | 5349.6 ± 47.4 | 5284.2 | 5424.8 | 19.84 ± 0.63 |

### 7 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-go` | 1.511 ± 0.020 | 1.490 | 1.556 | 1.00 |
| `bench-python` | 15.642 ± 0.540 | 14.876 | 16.494 | 10.35 ± 0.38 |
