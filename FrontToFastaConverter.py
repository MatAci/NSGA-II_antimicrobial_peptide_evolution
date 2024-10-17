import ast

with open('NSGA-II_antimicrobial_peptide_evolution\sequenceFiles\Doabr.txt', 'r') as file:
    lines = file.readlines()

with open('format.txt', 'w') as file:
    for i, line in enumerate(lines):
        # Parse the line as a Python literal
        data = ast.literal_eval(line.strip())
        # Extract the peptide sequence string
        peptide_sequence = data[1]
        # Write the peptide sequence to the file in FASTA format
        file.write(f'>{peptide_sequence}\n{peptide_sequence}\n')