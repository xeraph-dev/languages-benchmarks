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
| `bench-javascript` | 98.0 ± 1.1 | 97.0 | 100.0 | 7.07 ± 0.62 |
| `bench-go` | 13.9 ± 1.2 | 12.4 | 15.7 | 1.00 |
| `bench-python` | 250.9 ± 5.6 | 243.6 | 259.0 | 18.10 ± 1.61 |
| `bench-swift` | 80.7 ± 1.4 | 78.6 | 83.2 | 5.83 ± 0.51 |
| `bench-haskell` | 77.6 ± 1.8 | 74.3 | 80.3 | 5.60 ± 0.50 |

### 6 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 3.034 ± 0.032 | 3.011 | 3.120 | 9.95 ± 0.27 |
| `bench-go` | 0.305 ± 0.008 | 0.296 | 0.321 | 1.00 |
| `bench-python` | 2.975 ± 0.081 | 2.831 | 3.066 | 9.76 ± 0.36 |
| `bench-swift` | 2.653 ± 0.028 | 2.605 | 2.697 | 8.70 ± 0.24 |
| `bench-haskell` | 2.220 ± 0.028 | 2.184 | 2.266 | 7.28 ± 0.21 |

### 7 zeros

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `bench-javascript` | 17.313 ± 0.159 | 17.152 | 17.641 | 9.85 ± 0.18 |
| `bench-go` | 1.758 ± 0.027 | 1.719 | 1.808 | 1.00 |
| `bench-python` | 16.012 ± 0.399 | 15.104 | 16.415 | 9.11 ± 0.27 |
| `bench-swift` | 14.989 ± 0.175 | 14.735 | 15.313 | 8.53 ± 0.17 |
| `bench-haskell` | 16.624 ± 0.901 | 15.052 | 18.152 | 9.46 ± 0.53 |
