from Mutations import Mutations
import numpy as np
import os


if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')


GA = Mutations(
        length = 16,
        population_size = 20,
        num_generations = 15,
        subsequence = 'HK'
)

GA.calculate()

