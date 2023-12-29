#!/usr/bin/env bun

let secret = Bun.argv[2]
let zeros_count = +Bun.argv[3]

const getStartingZeros = arr => {
  let zeros = 0
  for (const byte of arr) {
    if (byte == 0x00) {
      zeros += 2
      continue
    }
    if (byte <= 0x0F) {
      zeros += 1
    }
    break
  }
  return zeros
}


for (let i = 0; ; i++) {
  const hash = Bun.MD5.hash(`${secret}${i}`)
  const zeros = getStartingZeros(hash)
  if (zeros === zeros_count) {
    console.log(i)
    break
  }
}