from ga import *
import os

# Variables
num_tournament = 5
num_parents_to_select = 2
individuals_to_exchange = 5
number_islands = 4
crossover_probability = [0.8, 0.9, 1.0, 0.9]
mutation_probability = [0.01, 0.05, 0.07, 0.08]
migration_probability = 0.2
population_size = 50
generations = 50
run_times = 1
features = ["EDGE_DENSITY", "AVG_DEGREE", "BURNING_NODES", "BURNING_EDGES", "NODES_IN_DANGER"]
heuristics = ["LDEG", "GDEG"]
number_rules = 10
seed = 100
number_firefighters = 1
# Creates a list of lists to save the different populations from the islands
population = [[]] * number_islands
training = True

# Tests
# =====================

fileName = [os.getcwd() + '\\instances\\Test\\100_ep0.05_0_gilbert_1.in']
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

# Paths to the problem instance and to the solution folder
experiment = 'Test'
folder_instance = os.getcwd() + '\\instances\\' + experiment
folder_solution = os.getcwd() + '\\experiments\\' + experiment
folder_name = str(population_size) + '-' + str(generations) + '-' + str(number_islands) + '-' + str(run_times)
folder_path = os.path.join(folder_solution, folder_name)

if not os.path.isdir(folder_path):
    os.makedirs(folder_path)

os.chdir(folder_path)
sub_folders = []
for folder in os.listdir():
    sub_folders.append(f"folder")

num_experiment = len(sub_folders)
if not os.path.isdir(str(num_experiment)):
    os.mkdir(str(num_experiment))
folder_path = os.path.join(folder_path, str(num_experiment))

os.chdir(folder_instance)
file_path = []
# Iterate over all the files in the directory
for file in os.listdir():
    # Create the filepath of particular file
    file_path.append(f"{folder_instance}\\{file}")

print(file_path)

hh = geneticAlgorithm(num_tournament, num_parents_to_select, individuals_to_exchange, number_islands, population,
                      population_size, generations, crossover_probability, mutation_probability,
                      migration_probability, features, heuristics, number_rules, seed, number_firefighters, False,
                      file_path, folder_path)

problem = FFP(file_path[0])
print("HH = " + str(problem.solve(hh, 1, False)))
