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

    def __init__(self, length, population_size, num_generations, subsequence, neutral, data):
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
        self.neutral = neutral
        self.data = data

    def generate_population(self, generation_number, population, flag):
        """
        Generate the population for the current generation.

        Parameters
        ----------
        generation_number : int
            The current generation number.
        insert_position : int or None, optional
            The starting position at which to insert the subsequence. If None, the position will be calculated.

        Returns
        -------
        list_of_peptide_objects : list of Peptide
            A list of Peptide objects for the current generation.
        """
        if generation_number == 1:
            # Generate a random population for the first generation
            if flag == 0:
                return self.generate_random_population(self.length-generation_number-len(self.subsequence)+1)
            else:
                return self.modify_existing_population(self.length-generation_number-len(self.neutral)+1)
        else:
            # Shift the subsequence for subsequent generations
            population_list = []

            # Load the population from the previous generation
            previous_population = population  # Placeholder for actual loading logic

            for peptide in previous_population:
                # Convert peptide string back to a list
                peptide_list = list(peptide.peptide_string)
                
                # Perform a left shift
                shifted_peptide = peptide_list[1:] + peptide_list[:1]
                
                # Append shifted peptide to the new population
                population_list.append(shifted_peptide)

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
    
    def modify_existing_population(self, insert_position=None):
        """
        Modify an existing population of peptides by inserting a subsequence.

        Parameters
        ----------
        existing_peptides : list of str
            A list of peptide sequences to modify.
        insert_position : int or None, optional
            The starting position at which to insert the subsequence. If None, the position will be random.

        Returns
        -------
        list_of_peptide_objects : list of Peptide
            A list of modified Peptide objects.
        """
        # Split data into lines and extract only the peptide strings
        lines = self.data.strip().split("\n")
        peptide_strings = [line.split(",")[0].strip() for line in lines]

        # Replace subsequence with neutral in each peptide string
        existing_peptides = [peptide.replace(self.subsequence, self.neutral) for peptide in peptide_strings]

        population_list = []

        for peptide in existing_peptides:
            peptide_list = list(peptide)  # Convert peptide string to a list for modification

            # Determine the starting index for the subsequence
            if insert_position is not None:
                if 0 <= insert_position <= len(peptide_list) - len(self.neutral):
                    start_index = insert_position
                else:
                    raise ValueError(f"Invalid insert_position: {insert_position}. Must be in range [0, {len(peptide_list) - len(self.neutral)}].")
            else:
                # Choose a random index if insert_position is not provided
                start_index = random.randint(0, len(peptide_list) - len(self.neutral))

            # Insert the subsequence at the determined position
            for i, char in enumerate(self.neutral):
                peptide_list[start_index + i] = char

            population_list.append(''.join(peptide_list))  # Convert back to string

        list_of_peptide_objects = []

        # Write modified peptides to 'in.txt'
        with open('in.txt', 'w') as file:
            for peptide in population_list:
                file.write(f'>{peptide}\n{peptide}\n')

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
        result : dict
            Dictionary containing statistics for each generation.
        """
        amp_threshold = 0.9
        toxicity_threshold = 1.0
        generation_number = 1
        population = []

        # Za statistiku
        generation_stats = []  # Lista gdje će svaki indeks predstavljati generaciju

        # Očisti datoteku na početku
        with open('subsequenceMutation/results.txt', 'w') as file:
            file.write('')  # Očisti sadržaj datoteke

        # Generacijska petlja
        while generation_number <= self.num_generations and (self.length - generation_number - len(self.subsequence) + 1) >= 0:
            print(f"Generation: {generation_number}/{self.num_generations}")

            # Generiraj populaciju
            # population = self.generate_random_population(self.length - generation_number - len(self.subsequence) + 1)
            # ako je flag 1 onda se radi alanin a ako je 0 onda se radi random
            population = self.generate_population(generation_number, population, 1)

            # Brojači za statistiku
            amp_count = 0
            toxicity_count = 0
            both_threshold_count = 0

            # Provjeri pragove za svaku sekvencu
            for peptide in population:
                if peptide.ff_amp_probability >= amp_threshold:
                    amp_count += 1
                if peptide.ff_toxicity >= toxicity_threshold:  
                    toxicity_count += 1
                if peptide.ff_amp_probability >= amp_threshold and peptide.ff_toxicity >= toxicity_threshold:
                    both_threshold_count += 1

            # Spremi statistiku za trenutnu generaciju
            generation_stats.append({
                'amp_count': amp_count,
                'toxicity_count': toxicity_count,
                'both_threshold_count': both_threshold_count
            })

            # Dodaj rezultate u datoteku
            with open('subsequenceMutation/results.txt', 'a') as file:
                for peptide in population:
                    file.write(f'{peptide.peptide_string}, {peptide.ff_amp_probability}, {peptide.ff_toxicity}\n')
                file.write(f'\n')

            generation_number += 1

        # Za Sekvencu HK daje HK--, -HK--, --HK-- ... a u result je ---HK, --HK-,--HK--...
        # Vraćamo statistiku za sve generacije
        return generation_stats



        
