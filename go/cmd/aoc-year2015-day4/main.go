package main

import (
	"crypto/md5"
	"fmt"
	"math/bits"
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

func uint64ToStrByte(x uint64) []byte {
	var digits [20]byte
	var currentDigit uint64
	var i int
	for i = 19; x != 0 && i >= 0; i-- {
		x, currentDigit = bits.Div64(0, x, 10)
		digits[i] = byte(currentDigit + 0x30)
	}
	return digits[i+1:]
}

func compute(prefix string, zeroes int) uint64 {
	var waitGroup sync.WaitGroup
	var writeLock sync.Mutex
	workerCount := runtime.NumCPU()

	bytePrefix := []byte(prefix)
	candidateSolution := uint64(0)
	keepGoing := true

	worker := func(start uint64, step uint64) {
		defer waitGroup.Done()
		hash := md5.New()
		for i := uint64(start); keepGoing || i < candidateSolution; i += step {
			hash.Write(bytePrefix)
			hash.Write(uint64ToStrByte(i))
			hashSum := hash.Sum(nil)
			hash.Reset()
			if getStartingZeroesCount(hashSum) >= zeroes {
				writeLock.Lock()
				if keepGoing || i < candidateSolution {
					candidateSolution = i
					keepGoing = false
				}
				writeLock.Unlock()
				return
			}
		}
	}

	waitGroup.Add(workerCount)
	for i := 0; i < workerCount; i++ {
		go worker(uint64(i), uint64(workerCount))
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
