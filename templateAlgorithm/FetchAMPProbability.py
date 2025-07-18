import subprocess
import numpy as np
import os

def fetchAMPProbability(peptides):

    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_file_path)     
    grandparent_dir = os.path.dirname(parent_dir)   

    sh_path = os.path.join(grandparent_dir, 'run_prediction.sh')
    
    #[['QC'],['YEW']]
    peptides = [[ ''.join(inner_list) ] for inner_list in peptides]
    #['QC', 'YEW']
    flattened_args = [item[0] for item in peptides]

    args = ['amp'] + flattened_args

    # Shell script for fetching AMP probability
    result = subprocess.run(
        [sh_path] + args,
        capture_output=True,
        text=True)

    # List of tuples (peptide_string, ff_amp_probability)
    peptide_and_ff_amp_probability = [(line.split(',')[0], f"{float(line.split(',')[1]):.2f}") 
                                        for line in result.stdout.strip().split('\n')]
    
    return peptide_and_ff_amp_probability
