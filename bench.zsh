#!/usr/bin/env zsh

rm -rf benchmarks

timeout=30

typeset -A challenges

if [ -z "$1" ] || [[ "$1" == 'aoc-year2015-day4' ]]; then
  challenges[aoc-year2015-day4]='Advent of Code - Year 2015 - Day 4'
fi

if [ ! -z "$1" ]; then shift; fi

for challenge name in ${(kv)challenges}; do (
  typeset -A langs
  if [ -z "$*" ] || [[ " $* " =~ ' go ' ]]; then
    langs[go]="go/build/$challenge"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' php ' ]]; then
    langs[php]="php php/$challenge/main.php"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' python ' ]]; then
    langs[python]="python python/$challenge/main.py"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' rust ' ]]; then
    langs[rust]="rust/target/release/$challenge"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' swift ' ]]; then
    langs[swift]="swift/.build/release/$challenge"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' zig ' ]]; then
    langs[zig]="zig/zig-out/bin/$challenge"
  fi
  if [ -z "$*" ] || [[ " $* " =~ ' javascript ' ]]; then
    langs[javascript]="bun run javascript/$challenge/main.js"
  fi

  for case in .inputs/$challenge/*; do (
    echo "$name => $(basename $case)"

    input=$(cat "$case/$(ls "$case" | grep input)")
    output=$(cat "$case/$(ls "$case" | grep output)")

    benchs=""
    runs=()

    for lang bin in ${(kv)langs}; do
      func="bench-$lang() { timeout $timeout $bin $input | tr -d '\n' | grep -xq $output; }"
      eval "$func"
      if ! bench-"$lang"; then
        echo "$lang validation failed"
      else
        runs+=(bench-"$lang")
        if [ -z "$benchs" ]; then
          benchs="$func"
        else
          benchs="$benchs;$func"
        fi
      fi
    done

    runs="${runs[@]}"
    if [ -z "$runs" ]; then
      echo "no benchmark to do"
      exit 1
    fi

    mkdir -p "benchmarks/$challenge"
    bash -c "$benchs; export -f $runs; hyperfine -w 1 -r 10 -i -S bash ${runs[@]} --export-markdown 'benchmarks/$challenge/$(basename $case).md'"
  ) done
) done