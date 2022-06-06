# Libraries
from tqdm import tqdm
from numpy.random import randint
from numpy import concatenate
from DummyHH import *

global current_state


def fitness(population):
    # how do I calculate the fitness of the HH???????
    return population


# Generate population
def generate_population(size, features, heuristics, nrules, seed, fileName, number_firefighters):
    new_population = []
    for i in range(size):
        individual = DummyHyperHeuristic(features, heuristics, nrules, seed, fileName)
        individual.fitness = individual.problem.solve(individual, number_firefighters, False)
        new_population.append(individual)
    return new_population


# Hacer el crossover entre cada regla.
def crossover(parentA, parentB, islands, crossover):
    if random.random() <= crossover[islands]:
        index_1, index_2 = randint(1, len(parentA) - 2, 2)
        if index_1 > index_2:
            temp = index_1
            index_1 = index_2
            index_2 = temp
        offspring_a = concatenate((parentA[:index_1], parentB[index_1:index_2], parentA[index_2:])).tolist()
        offspring_b = concatenate((parentB[:index_1], parentA[index_1:index_2], parentB[index_2:])).tolist()
    else:
        offspring_a = parentA.copy()
        offspring_b = parentB.copy()
    return offspring_a, offspring_b


# Tournament selection
# =======================
def select(island, tSize, numParents, features, heuristics, nrules, current_state, population):
    parent_a = DummyHyperHeuristic(features, heuristics, nrules, current_state)
    parent_b = DummyHyperHeuristic(features, heuristics, nrules, current_state)
    for x in range(numParents):
        island_population = population[island].copy()
        winner = randint(len(island_population) - 1)
        rival = randint(len(island_population) - 1)
        individualWinner = island_population.pop(winner)
        individualRival = island_population.pop(rival)
        for i in range(tSize):
            if individualRival.fitness > individualWinner.fitness:
                winner = rival
            rival = randint(len(island_population) - 1)
            individualRival = island_population.pop(rival)
        if x == 0:
            parent_a = population[island][winner]
        else:
            parent_b = population[island][winner]
    return parent_a, parent_b


# Genetic algorithm
# =======================
# (num_tournament, num_parents_to_select, individuals_to_exchange, number_islands,
# run_times, list_items, population, population_size, generations, crossover_probability,
# mutation_probability, backpack_capacity, max_weight, best_Knapsack, table, data)
def geneticAlgorithm(tournament, parents, exchange, islands, population, size, generations, crossover,
                     mutation, migration, features, heuristics, nrules, seed, fileName, number_firefighters):
    global current_state
    # Random generating the populations of the islands
    # Need to parallelize this loop
    for x in range(islands):
        population[x] = generate_population(size, features, heuristics, nrules, seed, fileName, number_firefighters)
    current_state = population[0][0].problem
    # Runs the evolutionary process
    for i in tqdm(range(generations)):
        for island in range(islands):
            # Crossover
            new_population = []
            for _ in range(size // 2):
                parent_a, parent_b = select(island, tournament, parents, features, heuristics, nrules, current_state, population)
                offspring_a, offspring_b = crossover(parent_a, parent_b, island, crossover)
                weight_a, value_a, weight_b, value_b = fitness(offspring_a, offspring_b, list_items, max_weight)
                child_a = Knapsack(weight_a, value_a, offspring_a)
                child_b = Knapsack(weight_b, value_b, offspring_b)
                new_population.extend([child_a, child_b])
            population[island] = new_population

            # Mutation
            for index in range(size):
                individual, boolean = mutate(population[island][index], mutation[island], capacity)
                if boolean:
                    weight, value, _, _ = fitness(individual.getChromosome(), individual.getChromosome(), list_items,
                                                  max_weight)
                    population[island][index].chromosome = individual.getChromosome().copy()
                    population[island][index].value = value
                    population[island][index].totalWeight = weight

        sorted_population, best = sort_population(islands, population, best)
        rate = random.random() <= migration
        if islands > 1 and i != generations - 1 and rate:
            population = migrate(exchange, population, sorted_population, islands)
