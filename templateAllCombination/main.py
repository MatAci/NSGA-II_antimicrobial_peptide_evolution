from PeptideEvolutionNSGAII import NSGA_II
import numpy as np
import os


if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')


GA = NSGA_II(
    template="HKWHR--IYW"
)

# Funkcija za čitanje podataka iz tekstualne datoteke i izdvajanje top 5 kombinacija
def get_top_5_peptides(file_path):
    peptides = []
    
    # Otvori datoteku za čitanje
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            peptide_string = parts[0]
            amp_probability = float(parts[1])
            toxicity = float(parts[2])
            
            peptides.append((peptide_string, amp_probability, toxicity))
    
    # Sortiraj po AMP vjerojatnosti (opadajuće) i zatim po toksičnosti (opadajuće)
    sorted_peptides = sorted(peptides, key=lambda x: (x[1], x[2]), reverse=True)
    
    # Vrati top 5
    return sorted_peptides[:5]

# Poziv funkcije i ispis rezultata
top_5 = get_top_5_peptides('templateAllCombination/FinalResults.txt')

# Ispiši top 5
for peptide in top_5:
    print(f"Peptide: {peptide[0]}, AMP Probability: {peptide[1]}, Toxicity: {peptide[2]}")

