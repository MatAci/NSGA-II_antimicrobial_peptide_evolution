import ast

# This file converts data from FinalResults.txt to FASTA so further data can be explored

with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/analysis/front.txt', 'r') as file:
    lines = file.readlines()

with open('/home/mataci/Desktop/NSGA-II_antimicrobial_peptide_evolution/analysis/fasta.txt', 'w') as file:
    for i, line in enumerate(lines):
        # Parse the line as a Python literal
        data = ast.literal_eval(line.strip())
        # Extract the peptide sequence string
        peptide_sequence = data[1]
        # Write the peptide sequence to the file in FASTA format
        file.write(f'>{peptide_sequence}\n{peptide_sequence}\n')