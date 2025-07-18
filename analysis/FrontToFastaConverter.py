import ast

# This file converts data from front.txt to FASTA so further data can be explored

with open('analysis/front.txt', 'r') as file:
    lines = file.readlines()

with open('analysis/fasta.txt', 'w') as file:
    for i, line in enumerate(lines):
        # Parse the line as a Python literal
        data = ast.literal_eval(line.strip())
        # Extract the peptide sequence string
        peptide_sequence = data[1]
        # Write the peptide sequence to the file in FASTA format
        file.write(f'>{peptide_sequence}\n{peptide_sequence}\n')