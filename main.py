from ga import *
from hhs import read_hh
from graphs import graph
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
run_times = 30
features = ["EDGE_DENSITY", "AVG_DEGREE", "BURNING_NODES", "BURNING_EDGES", "NODES_IN_DANGER"]
heuristics = ["LDEG", "GDEG"]
number_rules = 10
seed = 100
number_firefighters = 1
# Creates a list of lists to save the different populations from the islands
population = [[]] * number_islands
training = False
hyperheuristic = False
heuristic = False

root = os.getcwd()
instance = 'GBRL'
folder_instance = os.getcwd() + '\\instances\\' + instance
os.chdir(folder_instance)
file_path = []
# Iterate over all the files in the directory
for file in os.listdir():
    # Create the filepath of particular file
    file_path.append(f"{folder_instance}\\{file}")
os.chdir(root)

if training:
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

    geneticAlgorithm(num_tournament, num_parents_to_select, individuals_to_exchange, number_islands, population,
                     population_size, generations, crossover_probability, mutation_probability,
                     migration_probability, features, heuristics, number_rules, seed, number_firefighters, False,
                     file_path, folder_path)

if hyperheuristic:
    results = open(os.getcwd() + '\\results\\' + 'hh_results_' + instance + '_' + str(number_firefighters)
                   + '.txt', 'a')
    HHs = read_hh(len(features), len(heuristics), number_rules, number_islands)
    for file in file_path:
        problem = FFP(file)
        for x in range(number_islands):
            for _ in tqdm(range(run_times)):
                results.write(str(problem.solve(HHs[x], number_firefighters, False)) + " ")
        results.write("\n")
    results.close()

if heuristic:
    results = open(os.getcwd() + '\\results\\' + 'heuristics_results_' + instance + '_' + str(number_firefighters)
                   + '.txt', 'a')
    for file in file_path:
        problem = FFP(file)
        for x in range(len(heuristics)):
            for _ in tqdm(range(run_times)):
                results.write(str(problem.solve(heuristics[x], number_firefighters, False)) + " ")
        results.write("\n")
    results.close()

graph(instance, number_firefighters, run_times, number_islands, len(heuristics), file_path)
