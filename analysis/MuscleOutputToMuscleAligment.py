# Open the input file (muscleOutput.txt) and the output file (muscleAlignment.txt)
with open("analysis/muscleOutput.txt", "r") as input_file, open("analysis/muscleAlignment.txt", "w") as output_file:
    for line in input_file:
        # Skip empty lines and headers
        if line.strip() and not line.startswith("CLUSTAL") and not line.startswith(" "):
            # Split the line into words by whitespace
            columns = line.split()
            if len(columns) >= 2:  # Check if there is a second column
                output_file.write(columns[1] + "\n")  # Write the second column to the new file
