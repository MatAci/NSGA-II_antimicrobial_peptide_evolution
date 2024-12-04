from collections import Counter

# Funkcija za čitanje sekvenci iz datoteke i uzimanje samo drugog stupca
def read_sequences_from_file(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # Početak čitanja od 3. retka (indeks 2)
        for line in lines[2:]:
            parts = line.split()
            if len(parts) > 1:
                # Drugi stupac je sekvenca koju želimo, uklanjamo '-'
                sequences.append(parts[1].replace('-', ''))  
    return ''.join(sequences)  # Spajanje svih sekvenci u jedan string


# Funkcija za pronalaženje najčešćih k-mers sekvenci za različite duljine
def find_most_frequent_kmers(sequences, k_values=[2, 3, 4, 5]):
    results = {}
    for k in k_values:
        kmers = [sequences[i:i+k] for i in range(len(sequences) - k + 1)]
        kmer_counts = Counter(kmers)  # Brojanje frekvencije svake k-mers sekvence
        results[k] = kmer_counts.most_common(5)  # Vraća 5 najčešćih k-mers sekvenci
    return results

# Glavna funkcija
def main():
    # Putanja do tvoje datoteke
    file_path = 'analysis/muscleOutput.txt'
    
    # Učitavanje sekvenci iz datoteke
    sequences = read_sequences_from_file(file_path)
    
    # Pronađi najčešće k-mers sekvence za duljine 2, 3, 4 i 5
    frequent_kmers = find_most_frequent_kmers(sequences)
    
    # Ispis najčešćih k-mers sekvenci za svaku duljinu
    for k, kmers in frequent_kmers.items():
        print(f"Najčešće {k}-znakovne sekvence:")
        for kmer, count in kmers:
            print(f"{kmer}: {count}")
        print()

# Pokretanje glavne funkcije
if __name__ == "__main__":
    main()
