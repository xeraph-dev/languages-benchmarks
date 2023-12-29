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
| `bench-javascript` | 99.8 ± 0.5 | 98.7 | 100.6 | 7.52 ± 0.44 |
| `bench-go` | 13.3 ± 0.8 | 12.4 | 15.0 | 1.00 |
| `bench-python` | 252.8 ± 5.9 | 244.3 | 262.3 | 19.05 ± 1.20 |
| `bench-swift` | 141.3 ± 0.6 | 140.5 | 142.3 | 10.65 ± 0.62 |
| `bench-haskell` | 77.9 ± 1.3 | 76.2 | 80.5 | 5.87 ± 0.36 |

### 6 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 3.093 ± 0.045 | 3.036 | 3.187 | 9.65 ± 0.42 |
| `bench-go` | 0.320 ± 0.013 | 0.305 | 0.347 | 1.00 |
| `bench-python` | 2.958 ± 0.123 | 2.810 | 3.255 | 9.23 ± 0.54 |
| `bench-swift` | 4.879 ± 0.091 | 4.794 | 5.098 | 15.23 ± 0.69 |
| `bench-haskell` | 2.262 ± 0.029 | 2.224 | 2.313 | 7.06 ± 0.30 |

### 7 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 17.546 ± 0.313 | 17.213 | 18.141 | 9.45 ± 1.15 |
| `bench-go` | 1.857 ± 0.223 | 1.759 | 2.489 | 1.00 |
| `bench-python` | 16.239 ± 0.722 | 14.814 | 17.150 | 8.74 ± 1.12 |
| `bench-swift` | 28.295 ± 0.455 | 27.789 | 29.222 | 15.24 ± 1.84 |
| `bench-haskell` | 14.243 ± 1.219 | 12.873 | 16.417 | 7.67 ± 1.13 |
