from PeptideEvolutionNSGAII import NSGA_II
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os


def visualize_pareto_fronts(pareto_fronts):

    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.title("Prikaz pareto fronti")
    plt.xlabel("Toksičnost (ff_toxicity)")
    plt.ylabel("Vjerojatnost postojanja AMP svojstva (ff_amp_probability)")

    colors = ["#" + ''.join([np.random.choice(list('0123456789ABCDEF')) for _ in range(6)])
              for _ in range(len(pareto_fronts))]

    for front_index, front in enumerate(pareto_fronts):
        for peptide in front:
            _, _, ff_amp_probability, ff_toxicity = peptide
            plt.scatter(ff_toxicity, ff_amp_probability, c=colors[front_index])

    plt.show()

from scipy import integrate

def calculate_hyperarea(pareto_front):
    # Sort the points by x value
    sorted_points = sorted(pareto_front, key=lambda x: x[2])
    
    # Separate the x and y values
    x_values = [point[2] for point in sorted_points]
    y_values = [point[3] for point in sorted_points]
    
    # Add the origin to the points
    x_values = [0] + x_values
    y_values = [0] + y_values
    
    # Calculate the hyperarea using the trapezoidal rule
    hyperarea = np.trapz(y_values, x_values)
    
    return hyperarea

if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')


GA = NSGA_II(
    lowerRange=8,
    upperRange=19,
    population_size=70,
    offspring_size=20,
    num_generations=10,
    num_solutions_tournament=5,
    mutation_probability=0.3,
    penalty_function_reducer=0.7
)

pareto_fronts = GA.calculate()

for solution in pareto_fronts[0]:
    print(solution)

with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/sequenceFiles/FinalResults.txt', 'w') as file:
    for solution in pareto_fronts[0]:
        file.write(str(solution) + '\n')

visualize_pareto_fronts(pareto_fronts)
hyperarea = calculate_hyperarea(pareto_fronts[0])

print(f"Hyperarea for current parameters: {hyperarea}")