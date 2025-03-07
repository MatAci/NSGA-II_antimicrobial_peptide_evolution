from Mutations import Mutations
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_generation_stats(generation_stats):
    # Ekstraktujemo vrednosti sa odgovarajućih polja u listi
    amp_counts = [entry['amp_count'] for entry in generation_stats]
    toxicity_counts = [entry['toxicity_count'] for entry in generation_stats]
    both_threshold_counts = [entry['both_threshold_count'] for entry in generation_stats]
    
    # Generišemo indeksne vrednosti za x-osu (0, 1, 2, ...)
    generations = list(range(len(generation_stats)))
    
    # Kreiranje figure i subgrapova
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # Graf za amp_count
    axs[0].plot(generations, amp_counts, marker='o', color='r', label='AMP Count')
    axs[0].set_title('AMP Count over threshold of 0.9')
    axs[0].set_xlabel('Generation')
    axs[0].set_ylabel('AMP Count')
    axs[0].legend()
    axs[0].xaxis.set_major_locator(MaxNLocator(integer=True)) 
    axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))

    # Graf za toxicity_count
    axs[1].plot(generations, toxicity_counts, marker='o', color='g', label='Toxicity Count')
    axs[1].set_title('Toxicity Count over threshold of 1.0')
    axs[1].set_xlabel('Generation')
    axs[1].set_ylabel('Toxicity Count')
    axs[1].legend()
    axs[1].xaxis.set_major_locator(MaxNLocator(integer=True)) 
    axs[1].yaxis.set_major_locator(MaxNLocator(integer=True))

    # Graf za both_threshold_count
    axs[2].plot(generations, both_threshold_counts, marker='o', color='b', label='Both Threshold Count')
    axs[2].set_title('Both Threshold Count over nominal values')
    axs[2].set_xlabel('Generation')
    axs[2].set_ylabel('Both Threshold Count')
    axs[2].legend()
    axs[2].xaxis.set_major_locator(MaxNLocator(integer=True)) 
    axs[2].yaxis.set_major_locator(MaxNLocator(integer=True))

    # Prikazivanje grafova
    plt.tight_layout()
    plt.show()

if os.path.exists('in.txt'):
    os.remove('in.txt')
if os.path.exists('front.txt'):
    os.remove('front.txt')

data = """
VFNCSRRDHRAWFEHK, 0.65, 0.52
WMAVMPRCGLCHPHHK, 0.39, 1.3
MRNIQKATNSVHAKHK, 0.11, 0.98
NLMMSQLLGMDHHQHK, 0.29, 1.66
EARNWDSVSFQNILHK, 0.93, 1.53
MRYRGVEAAGWIFCHK, 0.03, 1.04
WAMNFSEVYQNRIYHK, 0.52, 2.1
KWKEACKVMTRREEHK, 0.83, 0.11
GAGNKVRFCGEMIWHK, 0.47, 0.78
WIEYNTFRVVDVKIHK, 0.45, 1.1
SEEFDEKRNSDGLVHK, 0.78, 0.91
FDCVGRGHSHMCYKHK, 0.24, 0.03
ETPHKEMCRYANCQHK, 0.89, 0.51
QRQLEPNVAKRHFTHK, 0.91, 1.32
YPWFYIQTCDTHICHK, 0.81, 0.58
CPQCRYIRGVHAHNHK, 0.66, 0.57
FNAWGWDKGSNTPKHK, 0.63, 0.46
QLGSLDCKIFEMVWHK, 0.9, 1.61
RDRNHFYYNLYGAAHK, 0.88, 1.09
PAMNDYEVFGYAYRHK, 0.31, 1.17
"""

GA = Mutations(
        length = 16,
        population_size = 20,
        num_generations = 15,
        subsequence = 'HK',
        neutral = 'LI',
        data = data

)

generation_stats = GA.calculate()
reversed_array = generation_stats[::-1]
plot_generation_stats(reversed_array)