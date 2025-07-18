from PeptideEvolutionNSGAII import NSGA_II
import numpy as np
import os

# Function to read data from a text file and extract the top 5 combinations
def get_top_5_peptides(file_path):
    peptides = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue  # preskoči prazne linije

            parts = line.strip().split(', ')
            if len(parts) != 3:
                print(f"Warning: Skipping malformed line: {line.strip()}")
                continue

            try:
                peptide_string = parts[0]
                amp_probability = float(parts[1])
                toxicity = float(parts[2])
                peptides.append((peptide_string, amp_probability, toxicity))
            except ValueError:
                print(f"Warning: Could not convert to float in line: {line.strip()}")
                continue

    sorted_peptides = sorted(peptides, key=lambda x: (x[1], x[2]), reverse=True)
    return sorted_peptides[:5]



if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')

GA = NSGA_II(
    template="HKWHR--IYW"
)

GA.evaluate()

# Call the function and print the results
top_5 = get_top_5_peptides('templateAllCombination/results.txt')

# Print the top 5
for peptide in top_5:
    print(f"Peptide: {peptide[0]}, AMP Probability: {peptide[1]}, Toxicity: {peptide[2]}")
