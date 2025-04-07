package genetics

import (
	"math/rand"
)

type Creature interface {
	New() Creature
	Fitness() float64
	Mutate(strenght float64)
	Clone() Creature
}

type Simulator struct {
	Population       []Creature
	Creature         Creature
	mutationStrenght float64
	generationNumber int
}

func (s *Simulator) GetGenerationNumber() int {
	return s.generationNumber
}

func (s *Simulator) Initialize(population int, mutationStrenght float64) {
	s.generationNumber = 0
	s.mutationStrenght = mutationStrenght

	s.Population = make([]Creature, 0, population)

	for _ = range population {
		s.Population = append(s.Population, s.Creature.New())
	}
}

func (s *Simulator) Step() {

	// Select
	s.shuffle()
	mid := len(s.Population) / 2
	for i := range mid {
		if s.Population[i].Fitness() < s.Population[i+mid].Fitness() {
			s.Population[i] = s.Population[i+mid]
		}

		if s.Population[i].Fitness() > s.Population[0].Fitness() {
			s.Population[0], s.Population[i] = s.Population[i], s.Population[0]
		}
	}

	// Clone and Mutate
	for i := range mid {
		s.Population[i+mid] = s.Population[i].Clone()
		s.Population[i+mid].Mutate(s.mutationStrenght)
	}

	s.generationNumber++
}

func (s *Simulator) GetBestCreature() Creature {
	return s.Population[0]
}

func (s *Simulator) shuffle() {
	for i := range s.Population {
		j := rand.Intn(i + 1)
		s.Population[i], s.Population[j] = s.Population[j], s.Population[i]
	}
}
