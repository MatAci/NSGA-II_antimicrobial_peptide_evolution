from PeptideEvolutionNSGAII import NSGA_II
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

def visualize_pareto_fronts(pareto_fronts):
    # Force integer ticks on x-axis and y-axis.
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.title("Prikaz pareto fronti")
    plt.xlabel("Duljina puta")
    plt.ylabel("Abecedne greške")

    colors = ["#"+''.join([np.random.choice(list('0123456789ABCDEF')) for _ in range(6)])
              for _ in pareto_fronts]

    for front_index, front in enumerate(pareto_fronts):
        for _, ff_path_length, ff_order in front:
            plt.scatter(ff_path_length, ff_order, c=colors[front_index])
    plt.show()


GA = NSGA_II(
    lowerRange=8,
    upperRange=15,
    numberOfRandomlyGeneratedPeptides=30,
    population_size=30,
    offspring_size=10,
    num_generations=30,
    num_solutions_tournament=4,
    mutation_probability=0.1
)

pareto_fronts = GA.calculate()

visualize_pareto_fronts(pareto_fronts)

for solution in pareto_fronts[0]:
    print(solution)