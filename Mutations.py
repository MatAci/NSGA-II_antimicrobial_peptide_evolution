import random
from Constants import AMINO_ACIDS

def add_amino_acid(peptide):
    index = random.randint(0, len(peptide))
    new_amino_acid = random.choice(AMINO_ACIDS)
    peptide.insert(index, new_amino_acid)

    return peptide

def delete_amino_acid(peptide):
    index = random.randint(0, len(peptide) - 1)
    peptide.pop(index)

    return peptide

def swap_amino_acids(peptide):
    index1, index2 = random.sample(range(len(peptide)), 2)
    peptide[index1], peptide[index2] = peptide[index2], peptide[index1]

    return peptide

def exchange_amino_acid(peptide):
    index = random.randint(0, len(peptide) - 1)
    new_amino_acid = random.choice(AMINO_ACIDS)
    peptide[index] = new_amino_acid

    return peptide