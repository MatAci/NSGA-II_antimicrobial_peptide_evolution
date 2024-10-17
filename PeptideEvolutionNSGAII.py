#!/usr/bin/env python3


import numpy as np
import RandomGenerator
import FitnessFunctionScraper
import os
import Mutations


class NSGA_II:
    # A comprehensible NSGA-II paper: https://web.njit.edu/~horacio/Math451H/download/Seshadri_NSGA-II.pdf


    # Class Route is used to conveniently store all info about a solution.
    class Peptide:
        def __init__(self, peptide_list, peptide_string, ff_amp_probability):
            self.peptide_list = peptide_list
            self.peptide_string = peptide_string
            self.ff_amp_probability = ff_amp_probability

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
                 numberOfRandomlyGeneratedPeptides,
                 population_size,
                 offspring_size,
                 num_generations,
                 num_solutions_tournament,
                 mutation_probability
                 ):
        """Save the forwarded arguments.

        Parameters
        ----------
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
        """

        self.lowerRange = lowerRange
        self.upperRange = upperRange
        self.numberOfRandomlyGeneratedPeptides = numberOfRandomlyGeneratedPeptides
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.num_generations = num_generations
        self.num_solutions_tournament = num_solutions_tournament
        self.mutation_probability = mutation_probability


    def calculate(self):
        """Use NSGA-II to find the best pareto front.

        Parameters
        ----------
        cities_to_visit : list
            List of strings. Cities that need to be visited.

        Returns
        -------
        List of pareto fronts.
            Each pareto front is a list containing a tuple for each solution:
            
            (A path to visit all the cities,
             total distance that will be travelled,
             the number of breaches of the alphabetical order).
        """

        generation_number = 1
        population = self.generate_random_population(self.lowerRange, self.upperRange, self.numberOfRandomlyGeneratedPeptides)

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
                         solution.ff_amp_probability) for solution in pareto_front
                    ] for pareto_front in pareto_fronts
                ]


    def generate_random_population(self, lowerRange, upperRange, numberOfRandomlyGeneratedPeptides):
        peptides = RandomGenerator.generate_random_peptides(lowerRange, upperRange, numberOfRandomlyGeneratedPeptides)

        list_of_peptide_objects = []

        with open('in.txt', 'w') as file:
            for peptide in peptides:
                peptide_string = ''.join(peptide)
                file.write(f'>{peptide_string}\n{peptide_string}\n')


        peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        if os.path.exists('in.txt'):
            os.remove('in.txt')
        
        for peptide_string, ff_amp_probability in peptide_and_ff_amp_probability:
            list_of_peptide_objects.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability)))

        return list_of_peptide_objects


    def perform_non_dominated_sort(self, population):
        """Divide the population into pareto fronts.
    
        Parameters
        ----------
        population : list
            List of self.Route objects.
    
        Returns
        -------
        List of lists of self.Route objects.
            E.g., [[Route#1, Route#2, ...], ...]
        """
    
        # Create a dictionary to store the count of each peptide.
        peptide_counts = {}
        for peptide in population:
            peptide_string = peptide.peptide_string
            if peptide_string in peptide_counts:
                peptide_counts[peptide_string] += 1
            else:
                peptide_counts[peptide_string] = 1
    
        # Add a penalty to the fitness function value of peptides that occur more than once.
        for peptide in population:
            peptide_string = peptide.peptide_string
            count = peptide_counts[peptide_string]
            if count > 1:
                penalty = count * 0.2  # Adjust the penalty factor as needed.
                peptide.ff_amp_probability -= penalty
    
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
    
                # Check if one solutions dominates over the other, or they
                # are equal.
    
                if population[i].ff_amp_probability >= population[j].ff_amp_probability:
                    # In this case, population[i] dominates over population[j].
                    list_of_dominated_indices[i].append(j)
                elif population[j].ff_amp_probability > population[i].ff_amp_probability:
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
            List of self.Route objects.
        """
        sorted_front_ff_amp_probability = sorted(
            pareto_front,
            key=lambda solution: solution.ff_amp_probability
        )

        # First and last solution in the sorted arrays have infinite
        # crowding distance because they only have one neighbour.
        sorted_front_ff_amp_probability[0].distance = np.inf
        sorted_front_ff_amp_probability[-1].distance = np.inf

        # Calculate maximum distance for each fitness function separately.
        max_ff_amp_probability = sorted_front_ff_amp_probability[-1].ff_amp_probability - sorted_front_ff_amp_probability[0].ff_amp_probability

        if max_ff_amp_probability <= 0:
            max_ff_amp_probability = 1

        for i in range(1, len(pareto_front) - 1):
            # Contribution of ff_path_length
            sorted_front_ff_amp_probability[i].distance += (sorted_front_ff_amp_probability[i+1].ff_amp_probability - sorted_front_ff_amp_probability[i-1].ff_amp_probability) / max_ff_amp_probability


    def generate_offspring(self, population):
        """Generate offspring.

        Use self.offspring_size.

        Parameters
        ----------
        population : list
            List of self.Route objects.

        Returns
        -------
        List of self.Route objects.
            E.g., [Route#1, Route#2, ...]
        """

        offspring = []
        offspring_peptides = []

        # Generate a predefined number of individuals.
        for _ in range(self.offspring_size):
            offspring.append(self.generate_single_solution(population))

        with open('in.txt', 'w') as file:
            for peptide in offspring:
                peptide_string = ''.join(peptide)
                file.write(f'>{peptide_string}\n{peptide_string}\n')


        peptide_and_ff_amp_probability = FitnessFunctionScraper.scrape_fitness_function()
        
        if os.path.exists('in.txt'):
            os.remove('in.txt')

        for peptide_string, ff_amp_probability in peptide_and_ff_amp_probability:
            print("Peptide: ", peptide_string)
            offspring_peptides.append(self.Peptide(list(peptide_string), peptide_string, float(ff_amp_probability)))

        return offspring_peptides


    def generate_single_solution(self, population):
        """Generate a single child.

        Parameters
        ----------
        population : list
            List of self.Route objects.

        Returns
        -------
        self.Route object.
        """
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
            List of self.Route objects.

        Returns
        -------
        self.Route object.
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


    def mutate(self, child_city_list):
        randInt = np.random.randint(0, 4)
        print("Mutation type: ", randInt)

        if randInt == 0:
            child_city_list = Mutations.add_amino_acid(child_city_list)
        elif randInt == 1:
            child_city_list = Mutations.delete_amino_acid(child_city_list)
        elif randInt == 2:
            child_city_list = Mutations.swap_amino_acids(child_city_list)
        elif randInt == 3:
            child_city_list = Mutations.exchange_amino_acid(child_city_list)

        return child_city_list


    def next_generation(self, non_dominated_sorted_population):
        """Select individuals for the next generation.

        Use self.population_size.

        Parameters
        ----------
        non_dominated_sorted_population : List of lists of self.Route objects.
            E.g., [[Route#1, Route#2, ...], ...]

        Returns
        -------
        List of self.Route objects.
            E.g., [Route#1, Route#2, ...]
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
