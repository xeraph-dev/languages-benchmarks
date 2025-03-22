package main

import (
	"math/rand"
)

func GenerateRandom() Candidate {
	var colors []string = Shuffle([]string{"red", "green", "ivory", "yellow", "blue"})
	var nationalities []string = Shuffle([]string{"english", "spaniard", "ukrainian", "norwegian", "japanese"})
	var pets []string = Shuffle([]string{"dog", "snail", "fox", "horse", "zebra"})
	var drinks []string = Shuffle([]string{"coffee", "tea", "milk", "juice", "water"})
	var hobbies []string = Shuffle([]string{"dancing", "painting", "reading", "football", "chess"})

	var result Candidate

	for i := range len(colors) {
		house := House{
			Color:       colors[i],
			Nationality: nationalities[i],
			Pet:         pets[i],
			Drink:       drinks[i],
			Hobby:       hobbies[i],
		}

		result = append(result, &house)
	}

	return result
}

func GenerateChild(parent Candidate, mutationStrenght int) Candidate {
	var child Candidate

	for i := range len(parent) {
		house := House{
			Color:       parent[i].Color,
			Nationality: parent[i].Nationality,
			Pet:         parent[i].Pet,
			Drink:       parent[i].Drink,
			Hobby:       parent[i].Hobby,
		}

		child = append(child, &house)
	}

	Mutate(child, mutationStrenght)
	return child
}

func Mutate(candidate Candidate, strenght int) {
	for _ = range strenght {
		h1 := rand.Intn(len(candidate))
		h2 := rand.Intn(len(candidate))
		if h1 == h2 {
			continue
		}

		prop := rand.Intn(5)

		if prop == 0 {
			candidate[h1].Color, candidate[h2].Color = candidate[h2].Color, candidate[h1].Color
		} else if prop == 1 {
			candidate[h1].Drink, candidate[h2].Drink = candidate[h2].Drink, candidate[h1].Drink
		} else if prop == 2 {
			candidate[h1].Hobby, candidate[h2].Hobby = candidate[h2].Hobby, candidate[h1].Hobby
		} else if prop == 3 {
			candidate[h1].Nationality, candidate[h2].Nationality = candidate[h2].Nationality, candidate[h1].Nationality
		} else if prop == 4 {
			candidate[h1].Pet, candidate[h2].Pet = candidate[h2].Pet, candidate[h1].Pet
		} else {
			panic("WTF")
		}
	}
}

func Fitness(candidate Candidate) int {
	fitness := 0
	houses := len(candidate)

	// There are five houses
	if houses == 5 {
		fitness += 1
	}

	// The Englishman lives in the red house
	for i := range houses {
		if candidate[i].Nationality == "english" {
			if candidate[i].Color == "red" {
				fitness += 1
			}

			break
		}
	}

	// The Spaniard owns the dog.
	for i := range houses {
		if candidate[i].Nationality == "spaniard" {
			if candidate[i].Pet == "dog" {
				fitness += 1
			}

			break
		}
	}

	// 	The person in the green house drinks coffee.
	for i := range houses {
		if candidate[i].Color == "green" {
			if candidate[i].Drink == "coffee" {
				fitness += 1
			}

			break
		}
	}

	// The Ukrainian drinks tea.
	for i := range houses {
		if candidate[i].Nationality == "ukrainian" {
			if candidate[i].Drink == "tea" {
				fitness += 1
			}

			break
		}
	}

	// The green house is immediately to the right of the ivory house.
	for i := range houses {
		if candidate[i].Color == "green" {
			if i != 0 && candidate[i-1].Color == "ivory" {
				fitness += 1
			}
			break
		}
	}

	// The snail owner likes to go dancing.
	for i := range houses {
		if candidate[i].Pet == "snail" {
			if candidate[i].Hobby == "dancing" {
				fitness += 1
			}

			break
		}
	}

	// The person in the yellow house is a painter.
	for i := range houses {
		if candidate[i].Color == "yellow" {
			if candidate[i].Hobby == "painting" {
				fitness += 1
			}

			break
		}
	}

	// The person in the middle house drinks milk.
	if candidate[houses/2].Drink == "milk" {
		fitness += 1
	}

	// The Norwegian lives in the first house.
	if candidate[0].Nationality == "norwegian" {
		fitness += 1
	}

	// The person who enjoys reading lives in the house next to the person with the fox.
	for i := range houses {
		if candidate[i].Hobby == "reading" {
			if i != 0 && candidate[i-1].Pet == "fox" {
				fitness += 1
			} else if i != houses-1 && candidate[i+1].Pet == "fox" {
				fitness += 1
			}

			break
		}
	}

	// The painter's house is next to the house with the horse.
	for i := range houses {
		if candidate[i].Hobby == "painting" {
			if i != 0 && candidate[i-1].Pet == "horse" {
				fitness += 1
			} else if i != houses-1 && candidate[i+1].Pet == "horse" {
				fitness += 1
			}

			break
		}
	}

	// The person who plays football drinks orange juice.
	for i := range houses {
		if candidate[i].Hobby == "football" {
			if candidate[i].Drink == "juice" {
				fitness += 1
			}

			break
		}
	}

	// The Japanese person plays chess.
	for i := range houses {
		if candidate[i].Nationality == "japanese" {
			if candidate[i].Hobby == "chess" {
				fitness += 1
			}

			break
		}
	}

	// The Norwegian lives next to the blue house.
	for i := range houses {
		if candidate[i].Nationality == "norwegian" {
			if i != 0 && candidate[i-1].Color == "blue" {
				fitness += 1
			} else if i != houses-1 && candidate[i+1].Color == "blue" {
				fitness += 1
			}

			break
		}
	}

	return fitness
}

func Select(population []Candidate, count int) []Candidate {
	selected := make([]Candidate, 0, count)

	for _ = range count {
		bestFit := -1
		bestItem := -1

		for i, v := range population {
			if v == nil {
				continue
			}

			if fit := Fitness(v); fit > bestFit {
				if Contains(selected, population[i]) {
					population[i] = nil
					continue
				}

				bestFit = fit
				bestItem = i
			}
		}

		if bestItem != -1 {
			selected = append(selected, population[bestItem])
			population[bestItem] = nil
		}

	}

	return selected
}
