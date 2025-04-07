package main

import (
	"math/rand"
	"zebra/genetics"
)

type House struct {
	Color       string
	Nationality string
	Pet         string
	Drink       string
	Hobby       string
}

type ZebraPuzzle struct {
	Genes   []*House
	fitness float64
}

func (z *ZebraPuzzle) Fitness() float64 {
	if z.fitness != 0 {
		return z.fitness
	}

	genes := z.Genes

	fitness := 0.0
	houses := len(genes)

	// There are five houses, I shouldn't check this rule but whatever
	if houses == 5 {
		fitness += 1
	}

	// The Englishman lives in the red house
	for i := range houses {
		if genes[i].Nationality == "English" {
			if genes[i].Color == "Red" {
				fitness += 1
			}

			break
		}
	}

	// The Spaniard owns the dog.
	for i := range houses {
		if genes[i].Nationality == "Spaniard" {
			if genes[i].Pet == "Dog" {
				fitness += 1
			}

			break
		}
	}

	// 	The person in the green house drinks coffee.
	for i := range houses {
		if genes[i].Color == "Green" {
			if genes[i].Drink == "Coffee" {
				fitness += 1
			}

			break
		}
	}

	// The Ukrainian drinks tea.
	for i := range houses {
		if genes[i].Nationality == "Ukrainian" {
			if genes[i].Drink == "Tea" {
				fitness += 1
			}

			break
		}
	}

	// The green house is immediately to the right of the ivory house.
	for i := range houses {
		if genes[i].Color == "Green" {
			if i != 0 && genes[i-1].Color == "Ivory" {
				fitness += 1
			}
			break
		}
	}

	// The snail owner likes to go dancing.
	for i := range houses {
		if genes[i].Pet == "Snail" {
			if genes[i].Hobby == "Dancing" {
				fitness += 1
			}

			break
		}
	}

	// The person in the yellow house is a painter.
	for i := range houses {
		if genes[i].Color == "Yellow" {
			if genes[i].Hobby == "Painting" {
				fitness += 1
			}

			break
		}
	}

	// The person in the middle house drinks milk.
	if genes[houses/2].Drink == "Milk" {
		fitness += 1
	}

	// The Norwegian lives in the first house.
	if genes[0].Nationality == "Norwegian" {
		fitness += 1
	}

	// The person who enjoys reading lives in the house next to the person with the fox.
	for i := range houses {
		if genes[i].Hobby == "Reading" {
			if i != 0 && genes[i-1].Pet == "Fox" {
				fitness += 1
			} else if i != houses-1 && genes[i+1].Pet == "Fox" {
				fitness += 1
			}

			break
		}
	}

	// The painter's house is next to the house with the horse.
	for i := range houses {
		if genes[i].Hobby == "Painting" {
			if i != 0 && genes[i-1].Pet == "Horse" {
				fitness += 1
			} else if i != houses-1 && genes[i+1].Pet == "Horse" {
				fitness += 1
			}

			break
		}
	}

	// The person who plays football drinks orange juice.
	for i := range houses {
		if genes[i].Hobby == "Football" {
			if genes[i].Drink == "Juice" {
				fitness += 1
			}

			break
		}
	}

	// The Japanese person plays chess.
	for i := range houses {
		if genes[i].Nationality == "Japanese" {
			if genes[i].Hobby == "Chess" {
				fitness += 1
			}

			break
		}
	}

	// The Norwegian lives next to the blue house.
	for i := range houses {
		if genes[i].Nationality == "Norwegian" {
			if i != 0 && genes[i-1].Color == "Blue" {
				fitness += 1
			} else if i != houses-1 && genes[i+1].Color == "Blue" {
				fitness += 1
			}

			break
		}
	}

	z.fitness = fitness
	return fitness
}

func (z *ZebraPuzzle) New() genetics.Creature {
	var colors []string = shuffle([]string{"Red", "Green", "Ivory", "Yellow", "Blue"})
	var nationalities []string = shuffle([]string{"English", "Spaniard", "Ukrainian", "Norwegian", "Japanese"})
	var pets []string = shuffle([]string{"Dog", "Snail", "Fox", "Horse", "Zebra"})
	var drinks []string = shuffle([]string{"Coffee", "Tea", "Milk", "Juice", "Water"})
	var hobbies []string = shuffle([]string{"Dancing", "Painting", "Reading", "Football", "Chess"})

	genes := make([]*House, 0, 5)

	for i := range len(colors) {
		house := House{
			Color:       colors[i],
			Nationality: nationalities[i],
			Pet:         pets[i],
			Drink:       drinks[i],
			Hobby:       hobbies[i],
		}

		genes = append(genes, &house)
	}

	return &ZebraPuzzle{Genes: genes}
}

func (z *ZebraPuzzle) Mutate(strenght float64) {
	// Mutation consists swappping 1 random property between 2 random houses

	genes := z.Genes

	for _ = range int(strenght) {
		h1 := rand.Intn(len(genes))
		h2 := rand.Intn(len(genes))
		if h1 == h2 {
			continue
		}

		prop := rand.Intn(5)

		if prop == 0 {
			genes[h1].Color, genes[h2].Color = genes[h2].Color, genes[h1].Color
		} else if prop == 1 {
			genes[h1].Drink, genes[h2].Drink = genes[h2].Drink, genes[h1].Drink
		} else if prop == 2 {
			genes[h1].Hobby, genes[h2].Hobby = genes[h2].Hobby, genes[h1].Hobby
		} else if prop == 3 {
			genes[h1].Nationality, genes[h2].Nationality = genes[h2].Nationality, genes[h1].Nationality
		} else if prop == 4 {
			genes[h1].Pet, genes[h2].Pet = genes[h2].Pet, genes[h1].Pet
		} else {
			panic("WTF")
		}
	}
}

func (z *ZebraPuzzle) Clone() genetics.Creature {
	var genes []*House

	for i := range len(z.Genes) {
		house := House{
			Color:       z.Genes[i].Color,
			Nationality: z.Genes[i].Nationality,
			Pet:         z.Genes[i].Pet,
			Drink:       z.Genes[i].Drink,
			Hobby:       z.Genes[i].Hobby,
		}

		genes = append(genes, &house)
	}

	return &ZebraPuzzle{Genes: genes}
}

func shuffle[T any](slice []T) []T {
	for i := range slice {
		j := rand.Intn(i + 1)
		slice[i], slice[j] = slice[j], slice[i]
	}

	return slice
}
