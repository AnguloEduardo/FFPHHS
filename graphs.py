import os
import matplotlib.pyplot as plt


def graph(instance, number_firefighters, run_times, islands, len_heuristics, problems):
    x_label = ['island_1', 'island_2', 'island_3', 'island_4', 'LDEG', 'GDEG']
    data_temp, data = [], []
    results_hh = open(os.getcwd() + '\\results\\' + 'hh_results_' + instance + '_' +
                      str(number_firefighters) + '.txt', 'r')
    results_h = open(os.getcwd() + '\\results\\' + 'hh_results_' + instance + '_' +
                     str(number_firefighters) + '.txt', 'r')
    text_h = results_h.read()
    tokens_h = text_h.split()
    text_hh = results_hh.read()
    tokens_hh = text_hh.split()
    for file in problems:
        for _ in range(islands):
            for _ in range(run_times):
                data_temp.append(float(tokens_hh.pop(0)))
            data.append(list(data_temp))
            data_temp = []
        for _ in range(len_heuristics):
            for _ in range(run_times):
                data_temp.append(float(tokens_h.pop(0)))
            data.append(list(data_temp))
            data_temp = []
        name = file.split("\\")
        name = name[len(name) - 1].replace('.', '-')
        fig = plt.figure(figsize=(10, 7))
        fig.suptitle('Performance of Hyper-heuristics VS heuristics ', fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        ax.boxplot(data, labels=x_label)
        ax.set_title(name[len(name) - 1])
        ax.set_ylabel('% of burned nodes')
        plt.savefig('results\\graphs\\' + instance + '\\' + name + '.jpg')
        data = []


def first_column(instance, number_firefighters, run_times, islands, len_heuristics, problems):
    data_hh, data_h, names = [], [], []
    num_problems = list(range(1, len(problems) + 1))
    results_hh = open(os.getcwd() + '\\results\\' + 'hh_results_' + instance + '_' +
                      str(number_firefighters) + '.txt', 'r')
    results_h = open(os.getcwd() + '\\results\\' + 'hh_results_' + instance + '_' +
                     str(number_firefighters) + '.txt', 'r')
    text_h = results_h.read()
    tokens_h = text_h.split()
    text_hh = results_hh.read()
    tokens_hh = text_hh.split()
    for file in problems:
        '''
        for y in range(islands):
            for x in range(run_times):
                if x == 0 and y == 0:
                    data_hh.append(float(tokens_hh.pop(0)))
                else:
                    tokens_hh.pop(0)
                    '''
        for y in range(len_heuristics):
            for x in range(run_times):
                if x == 0 and y == 0:
                    data_h.append(float(tokens_h.pop(0)))
                else:
                    tokens_h.pop(0)
    #plt.plot(num_problems, data_hh, label='hyper-heuristics')
    plt.plot(num_problems, data_h, label='heuristics')
    plt.xlabel('Instances of ' + instance)
    plt.ylabel('% of burned nodes')
    plt.title('Performance of heuristics')
    plt.legend()
    plt.savefig('results\\h' + instance + '.jpg')
