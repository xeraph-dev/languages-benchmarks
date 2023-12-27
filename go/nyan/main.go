package main

import (
	"crypto/md5"
	"encoding/binary"
	"fmt"
	"os"
	"runtime"
	"strconv"
	"sync"
)

func compute(prefix string, zeroes int) int {
	candidateSolution := -1
	var waitGroup sync.WaitGroup
	workerCount := runtime.NumCPU()

	var compare1 uint64 = 0xFFFFFFFFFFFFFFFF
	var compare2 uint64 = 0xFFFFFFFFFFFFFFFF

	if zeroes < 16 {
		compare1 = compare1 >> (zeroes * 4)
	} else if zeroes < 32 {
		compare1 = 0
		compare2 = compare2 >> ((zeroes - 16) * 4)
	} else {
		compare1 = 0
		compare2 = 0
	}

	worker := func(start int, step int) {
		defer waitGroup.Done()

		for i := start; candidateSolution == -1 || i < candidateSolution; i += step {
			hash := md5.New()
			hash.Write([]byte(prefix + strconv.Itoa(i)))
			hashSum := hash.Sum(nil)
			hashNum1 := binary.BigEndian.Uint64(hashSum[0:8])
			hashNum2 := binary.BigEndian.Uint64(hashSum[8:16])
			if hashNum1 <= compare1 && hashNum2 <= compare2 {
				fmt.Printf("Zeroes: %v, Found: %v - %x\n", zeroes, prefix+strconv.Itoa(i), hashSum)
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
	var prefix string
	var zeroes int

	if len(os.Args) != 3 {
		fmt.Printf("Usage: %v prefix zeroes\n"+
			"No parameters specified, will use 'yzbqklnj 6'\n",
			os.Args[0])

		prefix = "yzbqklnj"
		zeroes = 6
	} else {
		prefix = os.Args[1]

		var err error
		zeroes, err = strconv.Atoi(os.Args[2])
		if err != nil {
			fmt.Printf("ERROR: '%v' is not an integer\n", os.Args[2])
			os.Exit(1)
		}
	}

	if zeroes > 32 || zeroes < 0 {
		fmt.Printf("ERROR: MD5 hashes can only have 0-32 zeroes\n")
		os.Exit(1)
	}

	solution := compute(prefix, zeroes)
	fmt.Printf("Solution: %v\n", solution)

}
