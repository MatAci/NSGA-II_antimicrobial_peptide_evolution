from PeptideEvolutionNSGAII import NSGA_II
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import os

"""
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
    num_generations=30,
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
"""

from Bio import pairwise2


def calculate_similarity_scores(population):
    scores = {}
    
    for i, target_seq in enumerate(population):
        total_similarity = 0
        count = 0
        
        for j, compare_seq in enumerate(population):
            if i != j:  
                # All possible aligments between 2 sequences
                alignments = pairwise2.align.globalxx(target_seq, compare_seq)

                # First is best because pairwise2 return sorted list by score
                best_alignment = alignments[0]

                # 0 and 1 are sequences and 2 is score
                score = best_alignment[2] 

                start_target = best_alignment[3]
                end_target = best_alignment[4]

                # Length of aligment
                alignment_length = end_target - start_target

                # Percentage similarity relative to the entire population
                percentage_similarity = (score / alignment_length) * 100 if alignment_length > 0 else 0
                
                total_similarity += percentage_similarity
                count += 1
        
        # Average similarity for given sequence
        average_similarity = total_similarity / count if count > 0 else 0
        scores[target_seq] = average_similarity
    
    return scores

# Populacija sekvenci
"""
population_sequences = [
    "DRLPRQIRMMQLPDAFCPTC",
    "ARLPRQIRRMMQLRDAFPT",
    "RWARIQQRMMQC",
    "PRLARIIYMRCLTC",
    "DRLPRQIRMMQQLPAVF",
    "PRLARIWRRCLC",
    "DRWYRAIYCMLTC",
    "MPRLARIYMMQLPAVTF",
    "ARLPRQIRRMMQLPAVF",
    "MPRLARIYMMQLPAVVT",
    "ARLPRQIRRMQLPDAFCPTC",
    "PRLARIYMRQLC",
    "MPRLARIYMMQLPAVTF",
    "ARLPRIQQMRCLTC",
    "DRWYRAIYMRCLTC",
    "MPRLARIYMMQLPAVVTF",
    "MPRLARIYMMQLPAVVT",
    "MPRLARIYMMQLPAVVT",
    "ARLPRQIRRCLC",
    "DRWQHWQQRMMQLC",
    "MPRLARIYMMTQLP",
    "MPRLAIYMRQQLPAVVT",
    "PRLARIYMRQQLPIAVVT",
    "PRLARIYRRMMQLPAVF",
    "PRRLARIYMMQLPAVTF",
    "DRRLARIYMQLPAVTF",
    "MPRLARIYMMQPRVVTF"
]
"""
population_sequences = [
    "DRLPRQIRMMQLPDAFCPTC",
    "ARLPRQIRRMMQLRDAFPT"]

# Izračunaj sličnosti
similarity_scores = calculate_similarity_scores(population_sequences)

# Prikaži rezultate
for seq, score in similarity_scores.items():
    print(f"Sequence: {seq}, Average Similarity Score: {score:.2f}%")
