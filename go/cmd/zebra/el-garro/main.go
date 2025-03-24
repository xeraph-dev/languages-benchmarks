package main

import (
	"fmt"
	"os"
	"time"
)

var Logging bool = true

func Solve(initialPopulation int, selectCount int, childrenCount int, newRandomCount int, mutationStrenght int, fitnessTarget int) {
	started := time.Now()

	population := make([]Candidate, 0, initialPopulation)
	for _ = range initialPopulation {
		population = append(population, GenerateRandom())
	}

	bestFit := 0
	generation := 0
	for {
		// The best candidates pass directly to the new generation
		population = Select(population, selectCount)

		// Periodic report
		if fit := Fitness(population[0]); fit > bestFit || generation%100 == 0 {
			bestFit = fit
			if Logging {
				fmt.Printf("Generation=%07d, BestFitness=%02d, TargetFitness=%02d, TimeElapsed=%v\n", generation, bestFit, fitnessTarget, time.Since(started))
			}
		}

		// Found a solution
		if bestFit >= fitnessTarget {
			waterDrinker := ""
			zebraOwner := ""

			if Logging {
				PrintCandidate(population[0])
			}

			for _, house := range population[0] {
				if house.Drink == "water" {
					waterDrinker = house.Nationality
				}

				if house.Pet == "zebra" {
					zebraOwner = house.Nationality
				}
			}

			fmt.Printf("\nResponse: The zebra is owned by the <%s> and the <%s> drinks water", zebraOwner, waterDrinker)

			break
		}

		// Reproduce and mutate
		for i := range len(population) {
			for _ = range childrenCount {
				population = append(population, GenerateChild(population[i], mutationStrenght))
			}
		}

		// Add some new random candidates
		for _ = range newRandomCount {
			population = append(population, GenerateRandom())
		}

		generation += 1

	}

}

func PrintCandidate(candidate Candidate) {
	fmt.Print("\nFitness target reached. Best candidate:\n\n")
	fmt.Println("   | Color      | Country    | Pet        | Drink      | Hobby      |")
	fmt.Println("---|------------|------------|------------|------------|------------|")

	for i, house := range candidate {
		fmt.Printf(
			"%02d | %s | %s | %s | %s | %s |\n",
			i+1,
			StringPad(house.Color, 10),
			StringPad(house.Nationality, 10),
			StringPad(house.Pet, 10),
			StringPad(house.Drink, 10),
			StringPad(house.Hobby, 10),
		)
	}
}

func main() {
	if len(os.Args) == 2 && os.Args[1] == "-s" {
		Logging = false
	}

	initialPopulation := 50000 // Big initial population adds diversity
	stablePopulation := 2000

	selected := int(float64(stablePopulation) * 0.05) // Keep the best 5% of the population
	random := int(float64(stablePopulation) * 0.05)   // Add diversity with a random 5%
	childrenPerParent := int(float64(stablePopulation-selected-random) / float64(selected))
	mutation := 5
	targetFitness := 15

	if Logging {
		fmt.Print(
			"\n| Population Breakdown  |",
			"\n| ----------------------|------------ ",
			"\n| Initial Population    | ", initialPopulation,
			"\n| Stable Population     | ", stablePopulation,
			"\n| Survivors             | ", selected,
			"\n| Randomized            | ", random,
			"\n| Children per Survivor | ", childrenPerParent,
			"\n| Mutation amount       | ", mutation,
			"\n\n",
		)
	}

	Solve(initialPopulation, selected, childrenPerParent, random, mutation, targetFitness)
}
