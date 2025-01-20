import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
from scipy.spatial import ConvexHull
from scipy.integrate import trapezoid
from scipy import integrate

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
    # Extract (ff_toxicity, ff_amp_probability) from the zero pareto_front
    points = [(pep[3], pep[2]) for pep in pareto_front]

    # Separate x and y values for easier handling
    x = np.array([point[0] for point in points])
    y = np.array([point[1] for point in points])

    # Filter points where x > 0 (i.e., to the right of the y-axis)
    filtered_points = [(x_val, y_val) for x_val, y_val in zip(x, y) if x_val > 0]
    
    if len(filtered_points) < 3:
        print("Not enough points to form a convex hull on the positive x-axis.")
        return

    # Separate the filtered points into x and y values
    filtered_x = np.array([point[0] for point in filtered_points])
    filtered_y = np.array([point[1] for point in filtered_points])

    # Sort points by x-values
    sorted_indices = np.argsort(filtered_x)
    filtered_x = filtered_x[sorted_indices]
    filtered_y = filtered_y[sorted_indices]

    # Add the origin (0, 0) to the left side of the hull for better visualization
    x_hull = np.array([0, *filtered_x])
    y_hull = np.array([1, *filtered_y])

    # Calculate area under the upper hull using the trapezoid method
    area = trapezoid(y_hull, x_hull)
    print(f"Površina ispod Convex hull krivulje: {area}")

    with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/sequenceFiles/FinalResults.txt', 'a') as file:  
        file.write(f"Hyperarea for convex hull: {area}\n")
    
    # Plot the results showing the upper hull boundary and filled area beneath it
    plt.plot(x_hull, y_hull, marker='o', linestyle='-', color='blue')
    plt.fill_between(x_hull, y_hull, color='lightblue', alpha=0.5)
    plt.title("Convex Hull Krivulja")
    plt.xlabel("Toksičnost (ff_toxicity)")
    plt.ylabel("Vjerojatnost postojanja AMP svojstva (ff_amp_probability)")
    plt.xlim(0, filtered_x.max())
    plt.ylim(0, 1)
    plt.grid(True)
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

def visulize_threshold_through_generations(similarity_threshold_values):

    # Generations: x-axis will be a range from 1 to the length of similarity_threshold_values
    generations = list(range(1, len(similarity_threshold_values) + 1))

    # Plotting threshold values across generations
    plt.plot(generations, similarity_threshold_values, marker='o', linestyle='-', color='b')
    plt.xlabel('Generacija')
    plt.ylabel('Threshold')
    plt.title('Threshold kroz generacije')
    plt.grid(True)
    plt.xticks(generations)
    plt.show()