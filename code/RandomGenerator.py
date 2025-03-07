import numpy as np
import random
import time
from code.Constants import AMINO_ACIDS

def generate_random_peptides(lowerRange, upperRange, numberOfRandomlyGeneratedPeptides):
    peptides = []

    while len(peptides) < numberOfRandomlyGeneratedPeptides:
        seed = int(time.time() + random.random())
        np.random.seed(seed)
        length = np.random.randint(lowerRange, upperRange + 1) 
        peptide_sequence = np.random.choice(AMINO_ACIDS, size=length, replace=True).tolist()
        if peptide_sequence not in peptides:
            peptides.append(peptide_sequence)
    
    return peptides
    