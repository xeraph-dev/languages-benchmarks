package main

import (
	"math/rand"
	"strings"
)

func Shuffle(slice []string) []string {
	for i := range slice {
		j := rand.Intn(i + 1)
		slice[i], slice[j] = slice[j], slice[i]
	}

	return slice
}

func StringPad(text string, maxlen int) string {
	if len(text) >= maxlen {
		return text[:maxlen]
	}

	return text + strings.Repeat(" ", maxlen-len(text))
}

func IsEqual(c1 Candidate, c2 Candidate) bool {
	for i := range len(c1) {
		if c1[i].Color != c2[i].Color {
			return false
		}

		if c1[i].Drink != c2[i].Drink {
			return false
		}

		if c1[i].Hobby != c2[i].Hobby {
			return false
		}

		if c1[i].Nationality != c2[i].Nationality {
			return false
		}

		if c1[i].Pet != c2[i].Pet {
			return false
		}
	}

	return true
}

func Contains(population []Candidate, candidate Candidate) bool {
	for _, v := range population {
		if IsEqual(v, candidate) {
			return true
		}
	}

	return false
}
