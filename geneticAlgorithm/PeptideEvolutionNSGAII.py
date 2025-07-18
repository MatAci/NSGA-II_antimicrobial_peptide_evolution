#!/usr/bin/env python3
import numpy as np
import geneticAlgorithm.PenaltyFunction as PenaltyFunction
import geneticAlgorithm.RandomGenerator as RandomGenerator
import geneticAlgorithm.FitnessFunctionScraper as FitnessFunctionScraper
import os
import time
import random
import geneticAlgorithm.Mutations as Mutations
import geneticAlgorithm.FetchAMPProbability as FetchAMPProbability

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
                 penalty_function_reducer,
                 flag
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
        self.flag = flag


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
        generation_number = 1
        population = self.generate_random_population(self.lowerRange, self.upperRange, self.population_size)

        non_dominated_sorted_population = self.perform_non_dominated_sort(population)

        for i, _ in enumerate(non_dominated_sorted_population):
            self.calculate_crowding_distance(non_dominated_sorted_population[i])

        while True:
            if generation_number > self.num_generations:
                break

            print('Generation: {}/{}'.format(generation_number, self.num_generations))
            
            # Generate offspring
            offspring = self.generate_offspring(population)
            population += offspring

            population = self.fetch_fitness_function_values(population)
 
            for solution in population:
                solution.reset()

            non_dominated_sorted_population = self.perform_non_dominated_sort(population)

            for i, _ in enumerate(non_dominated_sorted_population):
                self.calculate_crowding_distance(non_dominated_sorted_population[i])

            population = self.next_generation(non_dominated_sorted_population)
            generation_number += 1

        for solution in population:
            solution.reset()

        pareto_fronts = self.perform_non_dominated_sort(population)
        return [
            [
                (solution.peptide_list,
                 solution.peptide_string,
                 solution.ff_amp_probability,
                 solution.ff_toxicity) for solution in pareto_front
            ] for pareto_front in pareto_fronts
        ]


    def generate_random_population(self, lowerRange, upperRange, population_size):
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
        peptides = RandomGenerator.generate_random_peptides(lowerRange, upperRange, population_size)

        list_of_peptide_objects = []
        
        with open('in.txt', 'w') as file:
            for peptide in peptides:
                peptide_string = ''.join(peptide)
                file.write(f'>{peptide_string}\n{peptide_string}\n')

        # peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(peptides)
        toxicity = FitnessFunctionScraper.toxicity()
        
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        for (peptide_string, ff_amp_probability), (peptide_id, svm_score, prediction) in zip(peptide_and_ff_amp_probability, toxicity):
            list_of_peptide_objects.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability), float(svm_score)))

        return list_of_peptide_objects


    def perform_non_dominated_sort(self, population):
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

        if self.flag == True:
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

                amp_prob_diff = np.sign(population[i].ff_amp_probability - population[j].ff_amp_probability)
                toxicity_diff = np.sign(population[i].ff_toxicity - population[j].ff_toxicity)

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


    def generate_offspring(self, population):
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
            single_solutions_list.append(self.generate_single_solution(population))

        with open('in.txt', 'w') as file:
            for solution in single_solutions_list:
                peptide_string = ''.join(solution)
                file.write(f'>{peptide_string}\n{peptide_string}\n')
        
        toxicity = FitnessFunctionScraper.toxicity()
        
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        for (solution), (peptide_id, svm_score, prediction) in zip(single_solutions_list, toxicity):
            peptide_string = ''.join(solution)
            offspring.append(self.Peptide(solution,peptide_string,"",float(svm_score)))

        return offspring


    def fetch_fitness_function_values(self, population):

        list_of_peptides = [peptide.peptide_string for peptide in population]
        # peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        peptide_and_ff_amp_probability = FetchAMPProbability.fetchAMPProbability(list_of_peptides)

        for peptide_string, ff_amp_probability in peptide_and_ff_amp_probability:
            for peptide in population:
                if peptide.peptide_string == peptide_string: 
                    peptide.ff_amp_probability = float(ff_amp_probability)   

        return population


    def generate_single_solution(self, population):
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
        
        recombination_index = np.random.randint(0, len(first_parent))
        child_peptide_list = first_parent[:recombination_index] + second_parent[recombination_index:]
        
        if np.random.rand() < self.mutation_probability:
            child_peptide_list = self.mutate(child_peptide_list)
        
        return child_peptide_list


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

        randInt = np.random.randint(0, 4)

        if randInt == 0:
            child_peptide_list = Mutations.add_amino_acid(child_peptide_list)
            print("Mutation type: add_amino_acid")
        elif randInt == 1:
            child_peptide_list = Mutations.delete_amino_acid(child_peptide_list)
            print("Mutation type: delete_amino_acid")
        elif randInt == 2:
            child_peptide_list = Mutations.swap_amino_acids(child_peptide_list)
            print("Mutation type: swap_amino_acids")
        elif randInt == 3:
            child_peptide_list = Mutations.exchange_amino_acid(child_peptide_list)
            print("Mutation type: exchange_amino_acid")

        return child_peptide_list


    def next_generation(self, non_dominated_sorted_population):
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
                    pareto_front[-(self.population_size-len(next_generation)):]
                )
                break

        return next_generation