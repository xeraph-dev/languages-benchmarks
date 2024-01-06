package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
)

func compute(initialNumbers []int, iterations int) int {
	// A map is the sensible way to approach the problem
	// numbers := make(map[int]*[2]int)
	// But a map lookup is slower.
	// A contiguous memory block is faster, if you have the ram for it, so...
	// We use a mostly empty, huge slice
	sliceSize := max(slices.Max(initialNumbers), iterations) + 1
	numbers := make([]*[2]int, sliceSize)
	tailNumber := 0
	initialNumbersCount := len(initialNumbers)

	for turn := 1; turn <= iterations; turn++ {
		if turn <= initialNumbersCount {
			tailNumber = initialNumbers[turn-1]
		} else if tailNumberTurns := numbers[tailNumber]; tailNumberTurns[0] != 0 {
			tailNumber = tailNumberTurns[1] - tailNumberTurns[0]
		} else {
			tailNumber = 0
		}

		tailNumberTurns := numbers[tailNumber]
		if tailNumberTurns != nil {
			tailNumberTurns[0] = tailNumberTurns[1]
			tailNumberTurns[1] = turn
		} else {
			numbers[tailNumber] = &[2]int{0, turn}
		}
	}
	return tailNumber
}

func main() {
	if len(os.Args) < 3 {
		fmt.Printf("Usage: %v iterations initial_numbers\n", os.Args[0])
		os.Exit(1)
	}

	iterations, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Printf("'%v' is not a number\n", os.Args[1])
		os.Exit(1)
	}

	initialNumbers := make([]int, len(os.Args)-2)
	for i, value := range os.Args[2:] {
		initialNumbers[i], err = strconv.Atoi(value)
		if err != nil {
			fmt.Printf("'%v' is not a number\n", value)
			os.Exit(1)
		}
	}

	fmt.Println(compute(initialNumbers, iterations))
	os.Exit(0)
}
