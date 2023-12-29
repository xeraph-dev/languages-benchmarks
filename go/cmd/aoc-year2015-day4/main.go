package main

import (
	"crypto/md5"
	"fmt"
	"os"
	"runtime"
	"strconv"
	"sync"
)

func getStartingZeroesCount(slice []byte) (zeroes int) {
	for _, value := range slice {
		if value == 0x00 {
			zeroes += 2
			continue
		}
		if value <= 0x0F {
			zeroes++
		}
		break
	}
	return zeroes
}

func compute(prefix string, zeroes int) int {
	var waitGroup sync.WaitGroup
	workerCount := runtime.NumCPU()

	bytePrefix := []byte(prefix)
	candidateSolution := -1
	worker := func(start int, step int) {
		defer waitGroup.Done()
		hash := md5.New()
		for i := start; candidateSolution == -1 || i < candidateSolution; i += step {
			hash.Write(bytePrefix)
			hash.Write([]byte(strconv.Itoa(i)))
			hashSum := hash.Sum(nil)
			hash.Reset()
			if getStartingZeroesCount(hashSum) >= zeroes {
				candidateSolution = i
				return
			}
		}
	}

	waitGroup.Add(workerCount)
	for i := 0; i < workerCount; i++ {
		go worker(i, workerCount)
	}
	waitGroup.Wait()

	return candidateSolution
}

func main() {
	if len(os.Args) != 3 {
		fmt.Printf("Usage: %v prefix zeroes\n", os.Args[0])
		os.Exit(1)

	}

	prefix := os.Args[1]
	zeroes, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Printf("ERROR: '%v' is not an integer\n", os.Args[2])
		os.Exit(1)
	}

	if zeroes > 32 || zeroes < 0 {
		fmt.Printf("ERROR: MD5 hashes can only have 0-32 zeroes\n")
		os.Exit(1)
	}

	solution := compute(prefix, zeroes)
	fmt.Printf("%v\n", solution)
}
