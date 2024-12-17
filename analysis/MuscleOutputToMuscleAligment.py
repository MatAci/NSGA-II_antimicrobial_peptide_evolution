# Otvori ulaznu datoteku (muscleOutput.txt) i izlaznu datoteku (musclealignment.txt)
with open("analysis/muscleOutput.txt", "r") as input_file, open("analysis/muscleAlignment.txt", "w") as output_file:
    for line in input_file:
        # Preskoči prazne linije i zaglavlja
        if line.strip() and not line.startswith("CLUSTAL") and not line.startswith(" "):
            # Podijeli liniju na riječi prema prazninama
            columns = line.split()
            if len(columns) >= 2:  # Provjeri ima li drugi stupac
                output_file.write(columns[1] + "\n")  # Zapiši drugi stupac u novi file
