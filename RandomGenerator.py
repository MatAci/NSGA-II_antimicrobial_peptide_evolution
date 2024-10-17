import random
from Constants import AMINO_ACIDS

def generate_random_peptides(lowerRange, upperRange, numberOfRandomlyGeneratedPeptides):
    peptides = []
    for _ in range(numberOfRandomlyGeneratedPeptides):
        length = random.randint(lowerRange, upperRange)
        peptide_sequence = random.choices(AMINO_ACIDS, k=length)
        peptides.append(peptide_sequence)
    return peptides