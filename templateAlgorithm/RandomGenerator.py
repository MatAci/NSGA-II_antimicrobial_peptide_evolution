import numpy as np
import random
import time
from Constants import AMINO_ACIDS

def generate_random_peptides(size, numberOfRandomlyGeneratedPeptides, template):
    peptides_variable = []
    peptides_full = []

    variable_positions = [i for i, char in enumerate(template) if char == '-']
    num_variable_sites = len(variable_positions)

    while len(peptides_variable) < numberOfRandomlyGeneratedPeptides:
        seed = int(time.time() + random.random())
        np.random.seed(seed)

        random_sequence = np.random.choice(AMINO_ACIDS, size=num_variable_sites, replace=True).tolist()

        if random_sequence not in peptides_variable:
            peptides_variable.append(random_sequence)

            new_peptide = list(template)
            for i, pos in enumerate(variable_positions):
                new_peptide[pos] = random_sequence[i]

            peptides_full.append(new_peptide)

    return peptides_variable, peptides_full
    