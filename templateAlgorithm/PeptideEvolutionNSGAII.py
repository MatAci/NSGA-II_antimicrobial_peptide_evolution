#!/usr/bin/env python3

#add two numbers

import numpy as np
import PenaltyFunction as PenaltyFunction
import RandomGenerator as RandomGenerator
import FitnessFunctionScraper as FitnessFunctionScraper
import os
import time
import random
import Mutations as Mutations
import FetchAMPProbability as FetchAMPProbability

class NSGA_II:

    # Class Peptide is used to conveniently store all info about a solution.
    class Peptide:
        def __init__(self, peptide_list, peptide_string, ff_amp_probability, ff_toxicity):
            """Store information about a single solution.

                       Parameters
                       ----------
                       peptide_list : list
                           List of peptides aminoacids.
                           E.g. ['A','D','K','R','S','M','E','A','C'...]
                       peptide_string : string
                           Peptide label.
                       ff_amp_probability : float
                           The possibility that antimicrobial peptide have antimicrobial properties.
                       ff_toxicity : float
                           The SVM score of toxicity of the peptide.
                       average_similarity : float
                            Average similarity relative to entire population

                       """

            self.peptide_list = peptide_list
            self.peptide_string = peptide_string
            self.ff_amp_probability = ff_amp_probability
            self.ff_toxicity = ff_toxicity
            self.average_similarity = 0

            # When a solution is created, set its rank and crowding distance
            # to initial values.
            self.reset()

        def reset(self):
            """Reset rank and crowding distance to initial values."""
            self.rank = -1
            self.distance = 0

    def __init__(self,
                 lowerRange,
                 upperRange,
                 population_size,
                 offspring_size,
                 num_generations,
                 num_solutions_tournament,
                 mutation_probability,
                 penalty_function_reducer
                 ):
        """Save the forwarded arguments.

        Parameters
        ----------
        lowerRange : int
            The number of min individual length
        upperRange : int
            The number of max individual length
        population_size : int
            The number of individuals in the population.
        offspring_size : int
            The number of new individuals to create in each generation.
        num_generations : int
            The number of generations/iterations to run the algorithm for.
        num_solutions_tournament : int
            The number of individuals that are picked for tournament selection.
        mutation_probability : float
            The probability of a mutation occurring.
        penalty_function_reducer : float
            Number which is used for reducing AMP probability if sequences are the same.
        similarity_threshold_values : List
            Penalty threshold collected through generations for graph plotting
        start_time: float
            Timer for testing purposes
        """

        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.num_generations = num_generations
        self.num_solutions_tournament = num_solutions_tournament
        self.mutation_probability = mutation_probability
        self.penalty_function_reducer = penalty_function_reducer
        self.similarity_threshold_values = []
        self.start_time = time.time()


    def calculate(self):
        """Use NSGA-II to find the best pareto front.

        Parameters
        -------
        Returns
        -------
        List of pareto fronts.
            Each pareto front is a list containing 3 values for each solution:
            
            (Peptide aminoacids list,
             Peptide string,
             Value of fitness function that represent possibility of peptide having AMP properties).
        """
        # Očisti datoteku na početku
        with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/templateAlgorithm/FinalResults.txt', 'w') as file:
            file.write('')  # Očisti sadržaj datoteke
        generation_number = 1
        template = "HKWHR--IYW------"
        peptide_variable, population = self.generate_random_population(16, self.population_size, template)

        """
        for pep in population:
            print(
                f"{pep.peptide_list} {pep.peptide_string} {pep.ff_amp_probability} {pep.ff_toxicity}\n"
            )
        """
        non_dominated_sorted_population = self.perform_non_dominated_sort(population,False)

        for i, _ in enumerate(non_dominated_sorted_population):
            self.calculate_crowding_distance(non_dominated_sorted_population[i])

        while True:
            if generation_number > self.num_generations:
                break

            print('Generation: {}/{}'.format(generation_number, self.num_generations))
            
            # Generate offspring
            offspring = self.generate_offspring(population, template,peptide_variable)
            population += offspring

            population = self.fetch_fitness_function_values(population)

            with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/templateAlgorithm/FinalResults.txt', 'a') as file:
                file.write(f"Generacija: {generation_number}\n")  # Korištenje f-string za spajanje
                for peptide in population:
                    file.write(f'{peptide.peptide_string}, {peptide.ff_amp_probability}, {peptide.ff_toxicity}\n')
                file.write('\n')


            for solution in population:
                solution.reset()

            non_dominated_sorted_population = self.perform_non_dominated_sort(population)

            for i, _ in enumerate(non_dominated_sorted_population):
                self.calculate_crowding_distance(non_dominated_sorted_population[i])

            population = self.next_generation(non_dominated_sorted_population, peptide_variable, template)
            generation_number += 1

        for solution in population:
            solution.reset()

        pareto_fronts = self.perform_non_dominated_sort(population, False)
        return [
            [
                (solution.peptide_list,
                 solution.peptide_string,
                 solution.ff_amp_probability,
                 solution.ff_toxicity) for solution in pareto_front
            ] for pareto_front in pareto_fronts
        ]


    def generate_random_population(self, size, population_size, template):
        """Generate N random individuals within given range.

                Use self.population_size.

                Parameters
                -------
                lowerRange : int
                    Lower limit of sequence length.
                upperRange : int
                    Upper limit of sequence length.
                population_size : int
                    Population size.

                Returns
                -------
                List of self.Peptide objects.
                """
        #[['Q', 'C'], ['Y', 'E', 'W']]
        peptide_variable, peptides = RandomGenerator.generate_random_peptides(size, population_size, template)

        list_of_peptide_objects = []
        
        with open('in.txt', 'w') as file:
            for peptide in peptides:
                peptide_string = ''.join(peptide)
                file.write(f'>{peptide_string}\n{peptide_string}\n')

        # self.time_lapse("Unutar generate_random_population prije računanja AMP-a")
        # peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(peptides)
        # self.time_lapse("Unutar generate_random_population nakon AMP Prije toxictiy")
        toxicity = FitnessFunctionScraper.toxicity()
        # self.time_lapse("Unutar generate_random_population nakon toxicity")
        
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        for (peptide_string, ff_amp_probability), (peptide_id, svm_score, prediction) in zip(peptide_and_ff_amp_probability, toxicity):
            list_of_peptide_objects.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability), float(svm_score)))

        return peptide_variable, list_of_peptide_objects

    def perform_non_dominated_sort(self, population, flag = True):
        """Divide the population into pareto fronts.
    
        Parameters
        ----------
        population : list
            List of self.Peptide objects.
    
        Returns
        -------
        List of lists of self.Peptide objects.
            E.g., [[Peptide#1, Peptide#2, ...], ...]
        """

        if flag == True:
            self.similarity_threshold_values = PenaltyFunction.applyPenaltyFactor(population, self.penalty_function_reducer)

        
        # Create a dictionary to store the count and flag of each peptide.
        peptide_counts = {}
        for peptide in population:
            peptide_string = peptide.peptide_string
            if peptide_string in peptide_counts:
                peptide_counts[peptide_string]['count'] += 1
            else:
                peptide_counts[peptide_string] = {'count': 1, 'flag': True}  # Start with 'flag' as True for the first peptide

        # Add a penalty to the fitness function value of peptides that occur more than once.
        for peptide_string, data in peptide_counts.items():
            count = data['count']
            flag = data['flag']

            if count > 1:
                # Get all peptides that are the same
                duplicates = [peptide for peptide in population if peptide.peptide_string == peptide_string]
                
                for i, peptide in enumerate(duplicates):
                    if i == 0:
                        continue  
                    else:
                        peptide_counts[peptide_string]['flag'] = False
                    
                    # Penalize the 'ff_amp_probability' 90% for non-first peptides
                    penalty_amp = peptide.ff_amp_probability * 0.9
                    peptide.ff_amp_probability -= penalty_amp
                    
                    # Penalize the 'ff_toxicity' while keeping the sign intact for non-first peptides
                    if peptide.ff_toxicity > 0:
                        penalty_toxicity = peptide.ff_toxicity * 0.9
                        peptide.ff_toxicity -= penalty_toxicity  # Decrease positive toxicity
                    else:
                        penalty_toxicity = peptide.ff_toxicity * 0.9
                        peptide.ff_toxicity += penalty_toxicity  # Make negative toxicity more negative
        
        

        # list_of_dominated_indices[n] will store indices of solutions
        # population[n] dominates over.
        list_of_dominated_indices = [[] for _ in population]
    
        # domination_count[n] will store how many solutions dominate over
        # population[n].
        domination_count = np.zeros(len(population))
    
        pareto_fronts = [[]]
    
        for i, _ in enumerate(population):
            for j, _ in enumerate(population):
    
                if i == j:
                    continue
    
                # Check if one solution dominates over the other, or they
                # are equal.

                # amp_weight = 0.7
                # toxicity_weight = 0.3
    
                # amp_prob_diff = amp_weight * (population[i].ff_amp_probability - population[j].ff_amp_probability)
                # toxicity_diff = toxicity_weight * (population[i].ff_toxicity - population[j].ff_toxicity)
                amp_prob_diff = np.sign(population[i].ff_amp_probability - population[j].ff_amp_probability)
                toxicity_diff = np.sign(population[i].ff_toxicity - population[j].ff_toxicity)
                # if amp_prob_diff >= 0 and toxicity_diff <= 0:
                # elif amp_prob_diff < 0 and toxicity_diff > 0:



                if (amp_prob_diff > 0 and toxicity_diff >= 0) or (amp_prob_diff >= 0 and toxicity_diff > 0):
                    # In this case, population[i] dominates over population[j].
                    list_of_dominated_indices[i].append(j)
                elif amp_prob_diff < 0 and toxicity_diff < 0:
                    # In this case, population[j] dominates over population[i].
                    domination_count[i] += 1
    
            if domination_count[i] == 0:
                # Solution population[i] is not dominated by any other solution,
                # therefore it belongs to the first (best) pareto front.
                population[i].rank = 0
                pareto_fronts[0].append(i)
    
        i = 0
        # Iterate until each solution is assigned to a pareto front.
        while len(pareto_fronts[i]) > 0:
            # A list where solutions that belong to the next pareto front
            # will be saved.
            next_pareto_front = []
    
            # Iterate over solutions on the last pareto front.
            for j in pareto_fronts[i]:
                for k in list_of_dominated_indices[j]:
                    # Reduce domination count for the solutions that are dominated
                    # by the individuals on the current pareto front.
                    domination_count[k] -= 1
    
                    # If the solution is no longer dominated, that is, all the
                    # solutions that dominated over the current solution were
                    # deployed to pareto fronts, add current solution to the
                    # next pareto front.
                    if domination_count[k] == 0:
                        population[k].rank = i + 1
                        next_pareto_front.append(k)
    
            # Jump to next pareto front.
            i += 1
    
            # Add current pareto front to the list of all pareto fronts.
            pareto_fronts.append(next_pareto_front)
    
        # Last pareto front is empty (check 'while' condition above), so
        # we remove it.
        del pareto_fronts[-1]
    
        # Turn pareto front indices into objects; Replace index with the
        # corresponding object in 'population'.
    
        object_pareto_fronts = []
    
        for pareto_front in pareto_fronts:
            current_front = []
            for index in pareto_front:
                current_front.append(population[index])
            object_pareto_fronts.append(current_front)

        return object_pareto_fronts

    def calculate_crowding_distance(self, pareto_front):
        """Calculate crowding distance for a single pareto front.

        Crowding distance is calculated for each pareto front separately.
        This function modifies object parameters directly and returns nothing.

        Parameters
        ----------
        pareto_front : list
            List of self.Peptide objects.
        """
        sorted_front_ff_amp_probability = sorted(
            pareto_front,
            key=lambda solution: solution.ff_amp_probability
        )

        sorted_front_ff_toxicity = sorted(
            pareto_front,
            key=lambda solution: solution.ff_toxicity
        )

        # First and last solution in the sorted arrays have infinite
        # crowding distance because they only have one neighbour.
        sorted_front_ff_amp_probability[0].distance = np.inf
        sorted_front_ff_amp_probability[-1].distance = np.inf

        sorted_front_ff_toxicity[0].distance = np.inf
        sorted_front_ff_toxicity[-1].distance = np.inf

        # Calculate maximum distance for each fitness function separately.
        max_ff_amp_probability = sorted_front_ff_amp_probability[-1].ff_amp_probability - sorted_front_ff_amp_probability[0].ff_amp_probability
        max_ff_toxicity = sorted_front_ff_toxicity[-1].ff_toxicity - sorted_front_ff_toxicity[0].ff_toxicity


        if max_ff_amp_probability <= 0:
            max_ff_amp_probability = 1

        if max_ff_toxicity <= 0:
            max_ff_toxicity = 1

        for i in range(1, len(pareto_front) - 1):
            # Contribution of ff_path_length
            sorted_front_ff_amp_probability[i].distance += (sorted_front_ff_amp_probability[i+1].ff_amp_probability - sorted_front_ff_amp_probability[i-1].ff_amp_probability) / max_ff_amp_probability
            sorted_front_ff_toxicity[i].distance += (sorted_front_ff_toxicity[i+1].ff_toxicity - sorted_front_ff_toxicity[i-1].ff_toxicity) / max_ff_toxicity

    def generate_offspring(self, population, template, peptide_variable):
        """Generate offspring.

        Use self.offspring_size.

        Parameters
        ----------
        population : list
            List of self.Peptide objects.

        Returns
        -------
        List of self.Peptide objects.
            E.g., [Peptide#1, Peptide#2, ...]
        """

        offspring = []
        single_solutions_list = []

        # Generate a predefined number of individuals.
        for _ in range(self.offspring_size):
            single_solutions_list.append(self.generate_single_solution(population, template))

        # Dodavanje novih varijabilnih dijelova u peptide_variable array
        peptide_variable.extend(single_solutions_list)

        # Pronađi indekse gdje su crtice '-' u templateu
        variable_positions = [i for i, char in enumerate(template) if char == '-']

        # Generiranje potpunih peptida spajanjem templatea s novim varijabilnim dijelovima
        full_peptides = []
        full_peptides_list = []
        for solution in single_solutions_list:
            new_peptide = list(template)
            for i, pos in enumerate(variable_positions):
                new_peptide[pos] = solution[i]  # Zamjena crtica varijabilnim dijelovima
            full_peptides_list.append(new_peptide)
            full_peptides.append(''.join(new_peptide))

        # Spremanje u datoteku
        with open('in.txt', 'w') as file:
            for peptide in full_peptides:
                file.write(f'>{peptide}\n{peptide}\n')

        # Dobivanje rezultata fitness funkcije
        toxicity = FitnessFunctionScraper.toxicity()

        # Brisanje datoteke nakon obrade
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        # Kreiranje konačne populacije objekata
        for solution, full_peptide, (peptide_id, svm_score, prediction) in zip(full_peptides_list, full_peptides, toxicity):
            offspring.append(self.Peptide(solution, full_peptide, "", float(svm_score)))

        return offspring

    def fetch_fitness_function_values(self, population):

        list_of_peptides = [peptide.peptide_string for peptide in population]
        # peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(list_of_peptides)
        # self.time_lapse("Unutar generate_offspring nakon računanja AMP-a prije toxicity-a")

        for peptide_string, ff_amp_probability in peptide_and_ff_amp_probability:
            # Pronađi odgovarajući peptid u populaciji i ažuriraj njegove vrijednosti
            for peptide in population:
                if peptide.peptide_string == peptide_string: 
                    peptide.ff_amp_probability = float(ff_amp_probability)   

        return population

    def generate_single_solution(self, population , template):
        """Generate a single child.

        Parameters
        ----------
        population : list
            List of self.Peptide objects.

        Returns
        -------
        self.Peptide object.
        """
        seed = int((time.time() + random.random()) * 1000) % (2**32)
        np.random.seed(seed)

        first_parent = self.tournament_select_parent(population).peptide_list
        second_parent = self.tournament_select_parent(population).peptide_list

        # Pronađi indekse gdje se nalaze crtice '-' u templateu
        variable_positions = [i for i, char in enumerate(template) if char == '-']

        # Izvuci varijabilni dio iz oba parenta na temelju templatea
        first_variable_part = [first_parent[i] for i in variable_positions]
        second_variable_part = [second_parent[i] for i in variable_positions]
        
        recombination_index = np.random.randint(0, len(first_parent))
        child_variable_part = first_variable_part[:recombination_index] + second_variable_part[recombination_index:]
        
        if np.random.rand() < self.mutation_probability:
            child_variable_part = self.mutate(child_variable_part)
        
        return child_variable_part

    def tournament_select_parent(self, population):
        """Select one parent by tournament selection.

        Use self.num_solutions_tournament.

        Parameters
        ----------
        population : list
            List of self.Peptide objects.

        Returns
        -------
        self.Peptide object.
        """

        # Select a random parent.
        random_parent = population[np.random.randint(0, len(population))]

        for i in range(self.num_solutions_tournament-1):
            # Select random opponent.
            random_opponent = population[np.random.randint(0, len(population))]

            # Pick a winner.
            if random_opponent.rank < random_parent.rank or \
                (random_opponent.rank == random_parent.rank and random_opponent.distance > random_parent.distance):
                random_parent = random_opponent

        return random_parent

    def mutate(self, child_peptide_list):
        """Mutate a child.

                This function modifies child peptide list and returns a new list.
                There are four possible functions for modification.

                Parameters
                ----------
                child_peptide_list : list,
                    List of peptide aminoacids.

                Returns
                -------
                List, A modified peptide aminoacids list.
                """

        randInt = np.random.randint(0, 3)

        if randInt == 0:
            child_peptide_list = Mutations.add_amino_acid(child_peptide_list)
            print("Mutation type: add_amino_acid")
        elif randInt == 1:
            child_peptide_list = Mutations.exchange_amino_acid(child_peptide_list)
            print("Mutation type: exchange_amino_acid")
        elif randInt == 2:
            child_peptide_list = Mutations.swap_amino_acids(child_peptide_list)
            print("Mutation type: swap_amino_acids")


        return child_peptide_list

    def next_generation(self, non_dominated_sorted_population, peptide_variable, template):
        """Select individuals for the next generation.

        Use self.population_size.

        Parameters
        ----------
        non_dominated_sorted_population : List of lists of self.Peptide objects.
            E.g., [[Peptide#1, Peptide#2, ...], ...]

        Returns
        -------
        List of self.Peptide objects.
            E.g., [Peptide#1, Peptide#2, ...]
        """
        next_generation = []

        for pareto_front in non_dominated_sorted_population:
            if len(pareto_front) + len(next_generation) <= self.population_size:
                # If the whole pareto front fits into next generation, add it.
                next_generation.extend(pareto_front)
            elif self.population_size - len(next_generation) > 0:
                # Otherwise, add the individuals with the highest crowding distance
                # to preserve genetic diversity.
                pareto_front.sort(key=lambda solution: solution.distance)
                next_generation.extend(
                    pareto_front[-(self.population_size - len(next_generation)):]
                )
                break

        # Pronađi indekse gdje se nalaze crtice '-' u templateu
        variable_positions = [i for i, char in enumerate(template) if char == '-']

        # Funkcija za izdvajanje varijabilnog dijela iz peptida
        def extract_variable_part(peptide_sequence):
            return [peptide_sequence[i] for i in variable_positions]

        # Kreiraj listu varijabilnih dijelova odabrane sljedeće generacije
        next_variable_parts = [
            extract_variable_part(peptide.peptide_string) for peptide in next_generation
        ]

        # Ažuriraj peptide_variable tako da sadrži samo varijabilne dijelove odabranih jedinki
        peptide_variable[:] = next_variable_parts

        """
        print("Next Generation Peptides:")
        for pep in next_generation:
            print(
                f"{pep.peptide_list} {pep.peptide_string} {pep.ff_amp_probability} {pep.ff_toxicity}\n"
            )

        print("\nUpdated Peptide Variable Array:")
        for variable_part in peptide_variable:
            print(variable_part)
        """
        return next_generation
 
    def time_lapse(self,checkpoint_name="Checkpoint"):
 
        current_time = time.time() - self.start_time
        time_text = f"{current_time:.2f} sekundi - {checkpoint_name}\n"
        # Zapisujemo vreme u datoteku
        with open("time.txt", "a") as fajl:
            fajl.write(time_text)
