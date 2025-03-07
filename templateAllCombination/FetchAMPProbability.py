import subprocess
import numpy as np

def fetchAMPProbability(peptides):
    
    #[['QC'],['YEW']]
    peptides = [[ ''.join(inner_list) ] for inner_list in peptides]
    #['QC', 'YEW']
    flattened_args = [item[0] for item in peptides]

    args = ['amp'] + flattened_args
    # Poziv shell skripte za dobivanje AMP vjerojatnosti
    result = subprocess.run(
        ['/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/run_prediction.sh'] + args,
        capture_output=True,
        text=True)

    # List of tuples (peptide_string, ff_amp_probability)
    peptide_and_ff_amp_probability = [(line.split(',')[0], f"{float(line.split(',')[1]):.2f}") 
                                        for line in result.stdout.strip().split('\n')]
    
    return peptide_and_ff_amp_probability
