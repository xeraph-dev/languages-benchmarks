package main

import (
	"crypto/md5"
	"encoding/binary"
	"fmt"
	"strconv"
)

const compare uint32 = 4095

var inputHash = "bgvyzdsv"

func main() {
	for i := 0; ; i++ {
		h := md5.New()
		in := inputHash + strconv.Itoa(i)
		h.Write([]byte(in))
		b := h.Sum(nil)
		x := binary.BigEndian.Uint32(b[0:4])
		if x|compare == compare {
			fmt.Printf("%d", i)
			break
		}
	}
}
