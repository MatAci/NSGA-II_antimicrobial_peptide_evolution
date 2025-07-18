def find_subsequence_repeats(algorithms):
    common_subsequences = {}

    # Iteriraj kroz sve algoritme i njihove sekvence
    for alg_name, alg_data in algorithms.items():
        for seq_length, seq_dict in alg_data.items():
            # Za svaku sekvencu unutar trenutne duljine (2, 3, 4, 5 znakova)
            for seq, count in seq_dict.items():
                if seq not in common_subsequences:
                    common_subsequences[seq] = {"algorithms": {alg_name: count}, "contains": []}
                else:
                    # Ako je sekvenca već prisutna, ažuriraj broj ponavljanja za trenutni algoritam
                    if alg_name not in common_subsequences[seq]["algorithms"]:
                        common_subsequences[seq]["algorithms"][alg_name] = count
                
                # Provjeri ovu sekvencu u svim algoritmima i svim duljinama
                for other_alg_name, other_alg_data in algorithms.items():
                    if other_alg_name != alg_name:  # Ne uspoređuj s istim algoritmom
                        for other_seq_length, other_seq_dict in other_alg_data.items():
                            for other_seq, _ in other_seq_dict.items():
                                # Provjeri ako je trenutna sekvenca podsekvenca veće sekvence
                                if seq.strip() in other_seq.strip():
                                    common_subsequences[seq]["contains"].append((other_alg_name, other_seq))
    
    return common_subsequences

def convert_data_to_object(data):
    # Inicijalizacija rezultata kao prazan dictionary
    result = {}
    
    # Podjela podataka na različite dijelove prema "---"
    algorithms_data = data.strip().split("\n\n---\n\n")

    # Obrada svakog algoritma
    for idx, algorithm in enumerate(algorithms_data, start=1):
        # Inicijalizacija strukture za algoritam
        algorithm_name = f"Algoritam {idx}"
        result[algorithm_name] = {
            "2-znakovne": {},
            "3-znakovne": {},
            "4-znakovne": {},
            "5-znakovne": {}
        }
        
        # Razdvajanje podataka po linijama
        lines = algorithm.split("\n")
        
        current_category = None
        
        # Obrada svake linije podataka
        for line in lines:
            line = line.strip()  # Ukloni suvišne razmake sa početka i kraja linije
            if not line:  # Ako je linija prazna, preskoči je
                continue
            
            if line.startswith("Najčešće"):
                # Prepoznavanje kategorija sekvenci
                if "2-znakovne" in line:
                    current_category = "2-znakovne"
                elif "3-znakovne" in line:
                    current_category = "3-znakovne"
                elif "4-znakovne" in line:
                    current_category = "4-znakovne"
                elif "5-znakovne" in line:
                    current_category = "5-znakovne"
            else:
                # Obrada podataka unutar kategorije
                if current_category and ":" in line:
                    seq, count = line.split(":")
                    result[algorithm_name][current_category][seq.strip()] = int(count.strip())
    
    return result

def save_results_to_file(results, filename="analysis/resultFromFrequency.txt"):
    with open(filename, 'w') as file:
        for seq, data in results.items():
            # Ako lista "contains" je prazna, preskoči
            if not data["contains"]:
                continue
            
            # Ispis sekvence
            file.write(f"Podsekvenca: {seq}\n")
            
            # Ako postoje ponavljanja u algoritmima, ispiši ih
            if data["algorithms"]:
                file.write(f"  Ponavljanja u algoritmima:\n")
                for alg_name, count in data["algorithms"].items():
                    file.write(f"    {alg_name}: {count} puta\n")
            
            # Ako postoje podsekvence u "contains", ispiši ih
            if data["contains"]:
                file.write("  Sadržava u:\n")
                for contain_info in data["contains"]:
                    file.write(f"    Algoritam: {contain_info[0]}, Sekvenca: {contain_info[1]}\n")
            
            file.write("\n")  # Prazan red za odvajanje


# Učitavanje sadržaja datoteke
data_file_path = 'analysis/resultsFromAnalysis.txt'
with open(data_file_path, 'r') as file:
    file_content = file.read()

# Pretvorba podataka u željeni format
algorithms = convert_data_to_object(file_content)

"""
algorithms = {
    "Algoritam 1": {
        "2-znakovne": {"XY": 10, "B": 17, "EF": 15},
        "3-znakovne": {"PRF": 13, "MPRB": 11, "IYW": 9}
    },
    "Algoritam 2": {
        "2-znakovne": {"XY": 10, "AB": 9, "CD": 8, "EF": 7},
        "3-znakovne": {"XYZ": 10, "DEF": 8},
        "4-znakovne": {"ABCD": 5, "EFGH": 6}
    }
}
"""

# Pozivanje funkcije
common_subsequences = find_subsequence_repeats(algorithms)

save_results_to_file(common_subsequences)