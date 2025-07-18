from collections import Counter

# Function to read sequences from a file and extract only the second column
def read_sequences_from_file(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Start reading from the 3rd line (index 2)
        for line in lines[2:]:
            parts = line.split()
            if len(parts) > 1:
                # The second column is the sequence we want, remove '-'
                sequences.append(parts[1].replace('-', ''))  
    return ''.join(sequences)  # Concatenate all sequences into a single string

# Function to find the most frequent k-mer sequences for different lengths
def find_most_frequent_kmers(sequences, k_values=[2, 3, 4, 5]):
    results = {}
    for k in k_values:
        kmers = [sequences[i:i+k] for i in range(len(sequences) - k + 1)]
        kmer_counts = Counter(kmers)  # Count the frequency of each k-mer sequence
        results[k] = kmer_counts.most_common(5)  # Return the top 5 most frequent k-mers
    return results

# Main function
def main():
    # Path to your file
    file_path = 'analysis/muscleOutput.txt'
    
    # Load sequences from the file
    sequences = read_sequences_from_file(file_path)
    
    # Find the most frequent k-mer sequences for lengths 2, 3, 4, and 5
    frequent_kmers = find_most_frequent_kmers(sequences)
    
    # Print the most frequent k-mer sequences for each length
    for k, kmers in frequent_kmers.items():
        print(f"Most frequent {k}-mer sequences:")
        for kmer, count in kmers:
            print(f"{kmer}: {count}")
        print()

# Run the main function
if __name__ == "__main__":
    main()
