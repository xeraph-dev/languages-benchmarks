package main

import (
	"fmt"
	"strings"
	"time"
	"zebra/genetics"
)

func Solve(population int, mutationStrenght float64, targetFitness float64) {
	started := time.Now()

	simulator := genetics.Simulator{
		Creature: &ZebraPuzzle{},
	}

	simulator.Initialize(population, mutationStrenght)

	for {

		if simulator.GetGenerationNumber()%100 == 0 || simulator.GetBestCreature().Fitness() >= targetFitness {
			fmt.Printf("Generation=%07d, BestFitness=%05.2f, TargetFitness=%05.2f, TimeElapsed=%v\n",
				simulator.GetGenerationNumber(),
				simulator.GetBestCreature().Fitness(),
				targetFitness,
				time.Since(started),
			)
		}

		if simulator.GetBestCreature().Fitness() >= targetFitness {
			PrintCandidate(simulator.GetBestCreature().(*ZebraPuzzle))
			break
		}

		simulator.Step()
	}

}

func PrintCandidate(c *ZebraPuzzle) {
	candidate := c.Genes

	fmt.Print("\nFitness target reached. Best candidate:\n\n")
	fmt.Println("   | Color      | Country    | Pet        | Drink      | Hobby      |")
	fmt.Println("---|------------|------------|------------|------------|------------|")

	for i, house := range candidate {
		fmt.Printf(
			"%02d | %s | %s | %s | %s | %s |\n",
			i+1,
			stringPad(house.Color, 10),
			stringPad(house.Nationality, 10),
			stringPad(house.Pet, 10),
			stringPad(house.Drink, 10),
			stringPad(house.Hobby, 10),
		)
	}
}

func main() {
	population := 10000
	mutation := 1.0
	targetFitness := 15.0

	Solve(population, mutation, targetFitness)
}

func stringPad(text string, maxlen int) string {
	if len(text) >= maxlen {
		return text[:maxlen]
	}

	return text + strings.Repeat(" ", maxlen-len(text))
}
