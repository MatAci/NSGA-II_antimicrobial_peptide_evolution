from PeptideEvolutionNSGAII import NSGA_II
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from scipy.spatial import ConvexHull
from scipy.integrate import trapezoid
from scipy import integrate
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

def visualize_convex_hull(pareto_front):
    # Points extraction (ff_toxicity, ff_amp_probability) from zero pareto_front
    points = [(pep[3], pep[2]) for pep in pareto_front]

    # Separate x and y values for easier handling
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])

    # Determine the rightmost x value and use it as the upper-right boundary point
    x_max = x.max()
    x_hull = np.array([0, *x, x_max])
    y_hull = np.array([1, *y, 0])

    # Sort points by x-values to ensure correct ordering for the hull
    sorted_indices = np.argsort(x_hull)
    x_hull = x_hull[sorted_indices]
    y_hull = y_hull[sorted_indices]

    # Calculate area under the upper hull using the trapezoid method
    area = trapezoid(y_hull, x_hull)
    print(f"Površina ispod Convex hull krivulje: {area}")

    # Plot the results showing the upper hull boundary and filled area beneath it
    plt.plot(x_hull, y_hull, marker='o', linestyle='-')
    plt.fill_between(x_hull, y_hull, color='lightblue', alpha=0.5)
    plt.title("Convex hull krivulja")
    plt.xlabel("Toksičnost (ff_toxicity)")
    plt.ylabel("Vjerojatnost postojanja AMP svojstva (ff_amp_probability)")
    plt.xlim(0, x_max)
    plt.ylim(0, 1)
    plt.grid()
    plt.show()

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
    num_generations=30,
    num_solutions_tournament=5,
    mutation_probability=0.3,
    penalty_function_reducer=0.15
)

pareto_fronts = GA.calculate()

for solution in pareto_fronts[0]:
    print(solution)

hyperarea = calculate_hyperarea(pareto_fronts[0])
print(f"Hyperarea for current parameters: {hyperarea}")

with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/sequenceFiles/FinalResults.txt', 'w') as file:
    for solution in pareto_fronts[0]:
        file.write(str(solution) + '\n')

visualize_pareto_fronts(pareto_fronts)
visualize_convex_hull(pareto_fronts[0])