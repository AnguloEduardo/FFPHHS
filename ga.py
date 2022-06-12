# Libraries
from tqdm import tqdm
from numpy.random import randint
from numpy import concatenate
from DummyHH import *


# Generate population
def generate_population(size, features, heuristics, nrules, seed, fileName, number_firefighters):
    new_population = []
    for i in range(size):
        individual = DummyHyperHeuristic(features, heuristics, nrules, seed, fileName)
        individual.fitness = individual.problem.solve(individual, number_firefighters, False)
        new_population.append(individual)
    return new_population


def crossover(parentA, parentB, crossover_prob, len_features, len_heuristics, nrules):
    if random.random() <= crossover_prob:
        conditions_A = []
        conditions_B = []
        offspring_a = []
        offspring_b = []
        child_a_temp = []
        child_b_temp = []
        for x in range(len_features):
            lst_A = []
            lst_B = []
            for parameter in parentA:
                lst_A.append(parameter[x])
            for parameter in parentB:
                lst_B.append(parameter[x])
            conditions_A.append(list(lst_A))
            conditions_B.append(list(lst_B))
        for x in range(len_features):
            param_feature_a = conditions_A[x]
            param_feature_b = conditions_B[x]
            for y in range(len_heuristics):
                split = len(param_feature_a) // len_heuristics
                index = split // 2
                if y == 0:
                    rule_a = param_feature_a[:split]
                    rule_b = param_feature_b[:split]
                else:
                    rule_a = param_feature_a[split:]
                    rule_b = param_feature_b[split:]
                child_a = concatenate((rule_a[:index], rule_b[index:])).tolist()
                child_b = concatenate((rule_a[index:], rule_b[:index])).tolist()
                child_a_temp = concatenate((child_a_temp, child_a)).tolist()
                child_b_temp = concatenate((child_b_temp, child_b)).tolist()
        for x in range(nrules):
            temp_a = []
            temp_b = []
            for y in range(len_features):
                temp_a.append(child_a_temp[3 * x + y])
                temp_b.append(child_b_temp[3 * x + y])
            offspring_a.append(temp_a)
            offspring_b.append(temp_b)
    else:
        offspring_a = parentA.copy()
        offspring_b = parentB.copy()
    return offspring_a, offspring_b


# Tournament selection
# =======================
def select(island, tSize, numParents, features, heuristics, nrules, population):
    parent_a = DummyHyperHeuristic(features, heuristics, nrules)
    parent_b = DummyHyperHeuristic(features, heuristics, nrules)
    for x in range(numParents):
        island_population = population[island].copy()
        winner = randint(len(island_population) - 1)
        rival = randint(len(island_population) - 1)
        individualWinner = island_population.pop(winner)
        individualRival = island_population.pop(rival)
        for i in range(tSize):
            if individualRival.fitness < individualWinner.fitness:
                winner = rival
            rival = randint(len(island_population) - 1)
            individualRival = island_population.pop(rival)
        if x == 0:
            parent_a = population[island][winner]
        else:
            parent_b = population[island][winner]
    return parent_a, parent_b


# Mutation operator
# =======================
def mutate(individual, mRate, nrules, len_features):
    if random.random() <= mRate:
        i, j = random.sample(range(nrules), 2)
        rule_i, rule_j = individual.conditions[i], individual.conditions[j]
        for x in range(len_features):
            rule_i[x], rule_j[x] = rule_i[x] + 0.015, rule_j[x] + 0.015
        return individual, True
    return individual, False


def sort_population(islands, population, best):
    # Sorting Knapsacks by they value
    population_copy = population.copy()
    for i in range(islands):
        population_copy[i].sort(key=lambda x: x.fitness, reverse=True)
        # Keeping track of the best solution found on each island
        if population_copy[i][0].fitness < best[i].fitness:
            best[i] = population_copy[i][0]
    return population_copy, best


def migrate(exchange, population, sorted_population, islands):
    # Exchanging the best 'exchange' Knapsacks solutions of each island to another
    temp_firefighter = []
    for index_1 in range(exchange):
        temp_firefighter.append(sorted_population[0][index_1])
    for index_1 in range(islands - 1):
        index = random.sample(range(len(population[0])), exchange)
        for index_2 in range(exchange):
            population[index_1][index[index_2]] = sorted_population[index_1 + 1][index_2]
    index = random.sample(range(len(population[0])), exchange)
    for index_1 in range(exchange):
        population[islands - 1][index[index_1]] = temp_firefighter[index_1]
    return population


# Genetic algorithm
# =======================
# (num_tournament, num_parents_to_select, individuals_to_exchange, number_islands,
# run_times, list_items, population, population_size, generations, crossover_probability,
# mutation_probability, backpack_capacity, max_weight, best_Knapsack, table, data)
def geneticAlgorithm(tournament, parents, exchange, islands, population, size, generations, crossover_prob,
                     mutation, migration, features, heuristics, nrules, seed, number_firefighters, debug, file_path,
                     folder_path):
    best = []
    first_instance = file_path[0]
    table = open(folder_path + '\\' + 'table.txt', 'a')
    # Random generating the populations of the islands
    for x in tqdm(range(islands)):
        population[x] = generate_population(size, features, heuristics, nrules, seed, first_instance,
                                            number_firefighters)
    # Runs the evolutionary process
    for instance in file_path:
        best = [DummyHyperHeuristic(features, heuristics, nrules, seed, instance)] * islands
        table.write("Instance: {}\n".format(instance))
        for i in tqdm(range(generations)):
            table.write("Generation: {}\n".format(i + 1))
            for island in range(islands):
                # Crossover
                new_population = []
                for _ in range(size // 2):
                    parent_a, parent_b = select(island, tournament, parents, features, heuristics, nrules, population)
                    chromosome_a, chromosome_b = parent_a.conditions, parent_b.conditions
                    offspring_a, offspring_b = crossover(chromosome_a, chromosome_b, crossover_prob[island],
                                                         len(features), len(heuristics), nrules)
                    child_a = DummyHyperHeuristic(features, heuristics, nrules, instance)
                    child_b = DummyHyperHeuristic(features, heuristics, nrules, instance)
                    child_a.conditions, child_b.conditions = offspring_a, offspring_b
                    child_a.fitness = child_a.problem.solve(child_a, number_firefighters, debug)
                    child_b.fitness = child_b.problem.solve(child_b, number_firefighters, debug)
                    new_population.extend([child_a, child_b])
                population[island] = new_population

                # Mutation
                for index in range(size):
                    individual, boolean = mutate(population[island][index], mutation[island], nrules, len(features))
                    if boolean:
                        individual.fitness = individual.problem.solve(individual, number_firefighters, debug)
                        population[island][index] = individual

            sorted_population, best = sort_population(islands, population, best)
            rate = random.random() <= migration
            if islands > 1 and i != generations - 1 and rate:
                population = migrate(exchange, population, sorted_population, islands)

            for z in range(islands):
                table.write("{0:5.5f}\n".format(best[z].fitness))
                table.write("{}".format(best[z]))
                table.write("\n")

            table.close()
            table = open(folder_path + '\\' + 'table.txt', 'a')
