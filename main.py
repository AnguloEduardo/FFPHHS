from ga import geneticAlgorithm

# Variables
num_tournament = 5
num_parents_to_select = 2
individuals_to_exchange = 5
number_islands = 4
crossover_probability = [0.8, 0.9, 1.0, 0.9]
mutation_probability = [0.01, 0.05, 0.07, 0.08]
migration_probability = [0.0, 0.1, 0.2, 0.4, 0.8, 1.0]
population_size = 300
generations = 50
features = ["EDGE_DENSITY", "AVG_DEGREE", "BURNING_NODES"]
heuristics = ["LDEG", "GDEG"]
number_rules = 10
seed = 100
number_firefighters = 1
# Creates a list of lists to save the different populations from the islands
population = [[]] * number_islands


# Tests
# =====================

fileName = "instances/BBGRL/50_ep0.2_0_gilbert_1.in"
'''
# Solves the problem using heuristic LDEG and one firefighter
problem = FFP(fileName)
print("LDEG = " + str(problem.solve("LDEG", 10, False)))

# Solves the problem using heuristic GDEG and one firefighter
problem = FFP(fileName)
print("GDEG = " + str(problem.solve("GDEG", 10, False)))

# Solves the problem using a randomly generated dummy hyper-heuristic
problem = FFP(fileName)
seed = random.randint(0, 1000)
print(seed)
hh = DummyHyperHeuristic(["EDGE_DENSITY", "AVG_DEGREE", "BURNING_NODES", "BURNING_EDGES", "NODES_IN_DANGER"], ["LDEG", "GDEG"], 10, seed)
print(hh)
print("Dummy HH = " + str(problem.solve(hh, 10, False)))
'''
geneticAlgorithm(num_tournament, num_parents_to_select, individuals_to_exchange, number_islands, population,
                 population_size, generations, crossover_probability, mutation_probability, migration_probability,
                 features, heuristics, number_rules, seed, fileName, number_firefighters)
