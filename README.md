# Languages Benchmarks

> \[!IMPORTANT]
>
> - Don't cheat, create a real algorithm that solves the requested problem.
> - Use all the resources provided by the language and its standard library, including concurrency and multithreading.
>   - It's allowed to use official packages if the standard library doesn't have the needed feature.
> - FFI is not allowed; use only the native language features.
> - Compute the answer using brute force; don't use divide and conquer. However, splitting the algorithm into chunks is allowed, which is useful for threading.

---

> \[!NOTE]
>
> To add another language, create a new folder and a branch with the language's name. If the name contains symbols, like `C#`, use an alternative like `csharp`.

---

> Organize your subproject so that each challenge has its own executable file. For example:
>
> ```shell
> language/
>   challenge-1/
>     developer-1/
>       main.lang
>     developer-2/
>       main.lang
>   challenge-2/
>     developer-1/
>       main.lang
> ```

## Benchmarks

> [!IMPORTANT]
> The minimum python version supported is `3.12`

> [!NOTE]
> The benchmark statistics will be exported to the [bench.md](./bench.md) file

To run the benchmarks, execute the command from the repository's root directory

```shell
python -m bench
```

The output will be similar to the following, where `5/0/0/0` indicates `successes/fails/timeouts/skips`.

```
Advent of Code - Year 2015 - Day 4
  5 zeros
     go by el-garro       - mean ± σ     20.3ms ± 426.4μs
        5 runs - 5/0/0/0     min … max   19.8ms …  20.9ms

    zig by MoskitoSantana - mean ± σ     15.3ms ±   2.7ms
        5 runs - 5/0/0/0     min … max   10.8ms …  18.1ms

    Summary
      zig by MoskitoSantana ran
        1.3 ±  0.7 times faster than go by el-garro
```

## [Advent of Code - Year 2015 - Day 4](https://adventofcode.com/2015/day/4)

The program must accept two positional arguments

- the first, a string representing the secret key
- the second, an integer between 5 and 7 representing the number of zeros

Try locally with the inputs provided on the challenge page

Just compute the requested number and print it

## [Advent of Code - Year 2020 - Day 15](https://adventofcode.com/2020/day/15)

The program must accept positional arguments in the below way

- the first, an integer representing nth number spoken to determine
- the rest, a list of integers representing the starting numbers

Try locally with the inputs provided on the challenge page

Just compute the requested number and print it
