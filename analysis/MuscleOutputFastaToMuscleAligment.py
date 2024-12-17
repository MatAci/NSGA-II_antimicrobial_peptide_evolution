# Otvori ulaznu datoteku i izlaznu datoteku
with open("analysis/muscleOutput.txt", "r") as input_file, open("analysis/muscleAlignment.txt", "w") as output_file:
    for line in input_file:
        # Ukloni prazne retke i retke koji počinju s '>'
        if line.strip() and not line.startswith(">"):
            output_file.write(line.strip() + "\n")  # Zapiši redak u izlaznu datoteku
