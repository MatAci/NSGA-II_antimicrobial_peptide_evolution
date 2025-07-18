from geneticAlgorithm.PeptideEvolutionNSGAII import NSGA_II
import geneticAlgorithm.VisualizeData as VisualizeData
import numpy as np
import os


if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')

GA = NSGA_II(
    lowerRange=8,
    upperRange=19,
    population_size=70,
    offspring_size=20,
    num_generations=2,
    num_solutions_tournament=5,
    mutation_probability=0.05,
    penalty_function_reducer=0.15,
    flag = True # If flag is set to True apply penalty function, if False do not apply penalty function
)

pareto_fronts = GA.calculate()

for solution in pareto_fronts[0]:
    print(solution)

with open('geneticAlgorithmOutputFiles/results.txt', 'w') as file:
    file.write("Pareto fronts solutions:\n")
    for solution in pareto_fronts[0]:
        file.write(str(solution) + '\n')

VisualizeData.visualize_pareto_fronts(pareto_fronts[0])
VisualizeData.visualize_convex_hull(pareto_fronts[0])
similarity_threshold_values,similarity_min_values,similarity_max_values,similarity_mean_values = GA.similarity_threshold_values
VisualizeData.visulize_threshold_through_generations(similarity_mean_values)

print(similarity_mean_values)