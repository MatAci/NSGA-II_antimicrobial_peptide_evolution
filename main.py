from PeptideEvolutionNSGAII import NSGA_II
import VisualizeData
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
    num_generations=30,
    num_solutions_tournament=5,
    mutation_probability=0.05,
    penalty_function_reducer=0.15
)

pareto_fronts = GA.calculate()

for solution in pareto_fronts[0]:
    print(solution)

hyperarea = VisualizeData.calculate_hyperarea(pareto_fronts[0])
print(f"Hyperarea for current parameters: {hyperarea}")

with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/sequenceFiles/FinalResults.txt', 'w') as file:
    file.write("Pareto fronts solutions:\n")
    for solution in pareto_fronts[0]:
        file.write(str(solution) + '\n')
    file.write(f"Hyperarea for current parameters: {hyperarea}\n")

VisualizeData.visualize_pareto_fronts(pareto_fronts)
VisualizeData.visualize_convex_hull(pareto_fronts[0])
similarity_threshold_values,similarity_min_values,similarity_max_values,similarity_mean_values = GA.similarity_threshold_values
VisualizeData.visulize_threshold_through_generations(similarity_mean_values)

print(similarity_mean_values)