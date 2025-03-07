#!/usr/bin/env python3

import numpy as np
import FitnessFunctionScraper as FitnessFunctionScraper
import os
import FetchAMPProbability as FetchAMPProbability
from itertools import product
import itertools

class NSGA_II:
    class Peptide:
        def __init__(self, peptide_list, peptide_string, ff_amp_probability, ff_toxicity):
            self.peptide_list = peptide_list
            self.peptide_string = peptide_string
            self.ff_amp_probability = ff_amp_probability
            self.ff_toxicity = ff_toxicity
            self.reset()

        def reset(self):
            self.rank = -1
            self.distance = 0

    def __init__(self, template):
        self.template = template

    def all_combinations(self):
        TEMPLATE = self.template
        AMINO_ACIDS = list('ACDEFGHIKLMNPQRSTVWY')  # Popis svih aminokiselina
        # Pronađi pozicije "--" u TEMPLATE
        empty_sites = [i for i, char in enumerate(TEMPLATE) if char == '-']

        # Generiraj sve moguće kombinacije aminokiselina za mjesta "--"
        possible_combinations = itertools.product(AMINO_ACIDS, repeat=len(empty_sites))

        # Popis za pohranu svih generiranih peptida
        generated_peptides = []

        # Zamijeni "--" u predlošku s generiranim kombinacijama
        for combination in possible_combinations:
            peptide_list = list(TEMPLATE)  # Pretvori template u listu karaktera
            for idx, amino_acid in zip(empty_sites, combination):
                peptide_list[idx] = amino_acid  # Zamijeni "-" s odgovarajućim aminokiselinama
            generated_peptides.append(peptide_list)

        return generated_peptides

    def evaluate(self):
        peptides = self.all_combinations()
        chunk_size = len(peptides) // 5
        peptide_chunks = [peptides[i:i + chunk_size] for i in range(0, len(peptides), chunk_size)]

        list_of_peptide_objects = []
        all_peptide_and_ff_amp_probability = []  # Ovdje ćemo pohraniti rezultate AMP vjerojatnosti
        all_toxicity = []  # Ovdje ćemo pohraniti rezultate toksičnosti
        
        # Započni zapis u in.txt (samo jednom)
        for peptide_chunk in peptide_chunks:
            with open('in.txt', 'w') as file:
                for peptide in peptide_chunk:
                    peptide_string = ''.join(peptide)
                    file.write(f'>{peptide_string}\n{peptide_string}\n')

            peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(peptide_chunk)
            toxicity = FitnessFunctionScraper.toxicity()
            
            if os.path.exists('in.txt'):
                os.remove('in.txt')
            
            # Pohrani rezultate u globalne liste
            all_peptide_and_ff_amp_probability.extend(peptide_and_ff_amp_probability)
            all_toxicity.extend(toxicity)

        # Sada, nakon što su svi podaci pohranjeni, spojimo ih u jedan for loop
        for (peptide_string, ff_amp_probability), (peptide_id, svm_score, prediction) in zip(all_peptide_and_ff_amp_probability, all_toxicity):
            list_of_peptide_objects.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability), float(svm_score)))

        # Spremi rezultate
        with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/templateAllCombination/FinalResults.txt', 'w') as file:
            for peptide in list_of_peptide_objects:
                file.write(f'{peptide.peptide_string}, {peptide.ff_amp_probability}, {peptide.ff_toxicity}\n')
            file.write('\n')
