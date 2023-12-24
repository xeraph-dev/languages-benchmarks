package main

import (
	"crypto/md5"
	"encoding/binary"
	"fmt"
	"runtime"
	"strconv"
	"time"
)

const compare uint32 = 255

var inputHash = "yzbqklnj"

const MAX_INT = 2_147_483_647 // max int32? i think..

func main() {
	ssss := time.Now()

	cores := runtime.NumCPU()

	c := make(chan int, 1)
	start := 0
	result := MAX_INT

	for {
		for i := 0; i < cores; i++ {
			go iterate(start, start+1000, c)
			start = start + 1000
		}
		counter := 0
		for s := range c {
			if s != -1 && s < result {
				result = s
			}
			counter++
			if counter == cores {
				break
			}
		}
		if result != MAX_INT {
			break
		}
	}

	fmt.Printf("%d in %s", result, time.Since(ssss).String())
}

func iterate(start int, end int, c chan int) {
	for i := start; i < end; i++ {
		h := md5.New()
		in := inputHash + strconv.Itoa(i)
		h.Write([]byte(in))
		b := h.Sum(nil)
		x := binary.BigEndian.Uint32(b[0:4])
		if x|compare == compare {
			c <- i
			return
		}
	}
	c <- -1
}
