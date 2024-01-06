#!/usr/bin/env bash

set -Eeuo pipefail
trap cleanup SIGINT SIGTERM ERR EXIT

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
}

# constants
declare -r SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
declare -r SCRIPT_VERSION="0.0.1"
declare -r -A CHALLENGES=(
  ['aoc-year2015-day4']='Advent of Code - Year 2015 - Day 4'
  ['aoc-year2020-day15']='Advent of Code - Year 2020 - Day 15'
)
declare -r -a LANGUAGES=(go php python rust swift zig javascript haskell)
declare -r TIMEOUT=30

# command-line arguments
declare -a args=()
declare -a challenges=()
declare -a languages=()
declare -A cmds=()

# colors
declare RESET='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''

main() {
  rm -rf .benchmarks

  for challenge in "${challenges[@]}"; do
    define_cmd "$challenge"

    for case in .inputs/"$challenge"/*; do
      local input
      local output
      local funcs=()

      echo "${CHALLENGES[$challenge]} => $(basename "$case")"
      echo

      for file in "$case"/*; do
        if [[ "$(basename "$file")" =~ ^input ]]; then
          input="$(cat "$file")"
        fi
        if [[ "$(basename "$file")" =~ ^output ]]; then
          output="$(cat "$file")"
        fi
      done

      for language in "${languages[@]}"; do
        local func_name="bench-$language"
        local func="$func_name() { timeout $TIMEOUT ${cmds[$language]} $input | tr -d '\n' | grep -xq $output; }"
        eval "$func"
        funcs+=("$func_name")
      done

      mkdir -p ".benchmarks/$challenge"

      export -f "${funcs[@]}"
      hyperfine -w 3 -r 10 -S bash --sort mean-time --export-markdown ".benchmarks/$challenge/$(basename "$case").md" "${funcs[@]}"

      echo
      echo
    done

    unset "${cmds[@]}"
  done
}

usage() {
  cat <<EOF
USAGE
  $SCRIPT_NAME

OPTIONS
  -h, --help        Print this help and exit
  -v, --verbose     Print script debug info
  -V, --version     Print script version
      --no-color    Disable colors
  -c, --challenges  Challenges to benchmark
  -l, --languages   Languages to benchmark

EXAMPLES
  # Run all benchmarks for all languages
  $SCRIPT_NAME

  # Run challenge-1 and challenge-2 benchmarks for all languages
  $SCRIPT_NAME -c challenge-1,challenge-2

  # Run challenge-1 and challenge-2 benchmarks for lang-1 and lang-2
  $SCRIPT_NAME -c challenge-1,challenge-2 -l lang-1,lang-2
EOF
  exit
}

define_cmd() {
  local challenge="$1"

  cmds=(
    [go]="go/build/$challenge"
    [php]="php php/$challenge/main.php"
    [python]="python python/$challenge/main.py"
    [rust]="rust/target/release/$challenge"
    [swift]="swift/.build/release/$challenge"
    [zig]="zig/zig-out/bin/$challenge"
    [javascript]="bun run javascript/$challenge/main.js"
    [haskell]="haskell/.stack-work/dist/aarch64-osx/ghc-9.6.3/build/$challenge/$challenge"
  )
}

setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    # shellcheck disable=SC2034
    RESET='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1}
  msg "$msg"
  exit "$code"
}

error() {
  die "Error: $*"
}

check_argument() {
  if [ -z "$1" ] || [ "${1:0:1}" == "-" ]; then
    error "Argument for $1 is missing"
  fi
}

parse_params() {
  while (("$#")); do
    case "${1-}" in
    -h | --help) usage ;;
    -v | --verbose) set -x ;;
    -V | --version) die "$SCRIPT_NAME v$SCRIPT_VERSION" 0 ;;
    --no-color) NO_COLOR=1 ;;
    -c | --challenges)
      check_argument "$2"
      for challenge in $(echo "${2//,/ }" | xargs); do
        if [[ ! "${!CHALLENGES[*]}" =~ $challenge ]]; then
          error "Invalid challenge $challenge"
        fi
        if [[ "${challenges[*]}" =~ $challenge ]]; then
          error "Duplicated challenge $challenge"
        fi
        challenges+=("$challenge")
      done
      shift 2
      ;;
    -l | --languages)
      check_argument "$2"
      for language in $(echo "${2//,/ }" | xargs); do
        if [[ ! "${LANGUAGES[*]}" =~ $language ]]; then
          error "Invalid language $language"
        fi
        if [[ "${languages[*]}" =~ $language ]]; then
          error "Duplicated language $language"
        fi
        languages+=("$language")
      done
      shift 2
      ;;
    -?*) error "Unsupported flag $1" ;;
    *)
      args+=("${1}")
      shift
      ;;
    esac
  done
}

default_params() {
  if [[ -z "${challenges[*]}" ]]; then
    msg "No challenges defined, using all"
    for challenge in "${!CHALLENGES[@]}"; do
      challenges+=("$challenge")
    done
  fi
  if [[ -z "${languages[*]}" ]]; then
    msg "No languages defined, using all"
    for language in "${LANGUAGES[@]}"; do
      languages+=("$language")
    done
  fi
}

parse_params "$@"
setup_colors
default_params
main
