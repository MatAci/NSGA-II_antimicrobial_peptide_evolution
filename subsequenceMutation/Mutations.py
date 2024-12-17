import random
from Constants import AMINO_ACIDS
import FetchAMPProbability, FitnessFunctionScraper
import os

class Mutations:

    class Peptide:
        def __init__(self, peptide_list, peptide_string, ff_amp_probability, ff_toxicity):
            self.peptide_list = peptide_list
            self.peptide_string = peptide_string
            self.ff_amp_probability = ff_amp_probability
            self.ff_toxicity = ff_toxicity
            self.average_similarity = 0

    def __init__(self, length, population_size, num_generations, subsequence):
        """
        Initialize the NSGA_II class with the given parameters.

        Parameters
        ----------
        length : int
            The length of the sequences.
        population_size : int
            The number of individuals in the population.
        num_generations : int
            The number of generations/iterations to run the algorithm for.
        subsequence : str
            The subsequence to be used in the algorithm.
        """
        self.length = length
        self.population_size = population_size
        self.num_generations = num_generations
        self.subsequence = subsequence

    def generate_random_population(self, insert_position=None):
        """
        Generate a random population of peptides.

        Parameters
        ----------
        insert_position : int or None, optional
            The starting position at which to insert the subsequence. If None, the position will be random.

        Returns
        -------
        list_of_peptide_objects : list of Peptide
            A list of randomly generated Peptide objects.
        """
        population_list = []
        for _ in range(self.population_size):
            # Generate a random sequence of the given length
            peptide_list = [random.choice(AMINO_ACIDS) for _ in range(self.length)]

            # Determine the starting index for the subsequence
            if insert_position is not None:
                if 0 <= insert_position <= self.length - len(self.subsequence):
                    start_index = insert_position
                else:
                    raise ValueError(f"Invalid insert_position: {insert_position}. Must be in range [0, {self.length - len(self.subsequence)}].")
            else:
                # Choose a random index if insert_position is not provided
                start_index = random.randint(0, self.length - len(self.subsequence))

            # Insert the subsequence at the determined position
            for i, char in enumerate(self.subsequence):
                peptide_list[start_index + i] = char

            population_list.append(peptide_list)

        list_of_peptide_objects = []

        # Write peptides to 'in.txt'
        with open('in.txt', 'w') as file:
            for peptide in population_list:
                peptide_string = ''.join(peptide)
                file.write(f'>{peptide_string}\n{peptide_string}\n')

        # Fetch AMP probability and toxicity
        peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(population_list)
        toxicity = FitnessFunctionScraper.toxicity()

        # Remove 'in.txt' after fetching data
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        # Create peptide objects
        for (peptide_string, ff_amp_probability), (peptide_id, svm_score, prediction) in zip(peptide_and_ff_amp_probability, toxicity):
            list_of_peptide_objects.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability), float(svm_score)))

        return list_of_peptide_objects

    def calculate(self):
        """
        Perform the main NSGA-II algorithm.

        Returns
        -------
        result : str
            Placeholder return value.
        """
        generation_number = 1

        # Očisti datoteku na početku
        with open('subsequenceMutation/results.txt', 'w') as file:
            file.write('')  # Očisti sadržaj datoteke

        # Generacijska petlja
        while generation_number <= self.num_generations:
            print(f"Generation: {generation_number}/{self.num_generations}")
            population = self.generate_random_population(self.length-generation_number-2)

            # Dodaj rezultate u datoteku
            with open('subsequenceMutation/results.txt', 'a') as file:
                for peptide in population:
                    file.write(f'{peptide.peptide_string}, {peptide.ff_amp_probability}, {peptide.ff_toxicity}\n')
                file.write(f'\n')

            generation_number += 1


        
