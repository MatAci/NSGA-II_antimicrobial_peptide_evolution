from Bio import pairwise2
import numpy as np

similarity_threshold_values = []
similarity_min_values = []
similarity_max_values = []
similarity_mean_values = []


def calculate_penalty(similarities, min_sim, max_sim, penalty_factor_reducer, p=2.75):
    #Izračunava kazne prema kvadratnoj funkciji
    penalties = []
    for sim in similarities:
        # Normaliziraj sličnost
        norm_sim = (sim - min_sim) / (max_sim - min_sim) if max_sim > min_sim else 0
        # Primijeni kvadratnu kaznu
        penalty = (norm_sim ** p) * penalty_factor_reducer
        penalties.append(penalty)
    return penalties

def applyPenaltyFactor(population, penalty_function_reducer):
    global_similarities = [] 
    similarity_cache = {} 

    for i, target_obj in enumerate(population):
        target_seq = target_obj.peptide_string
        total_similarity = 0
        count = 0

        for j, compare_obj in enumerate(population):
            if i != j:
                compare_seq = compare_obj.peptide_string

                # Unique key (i, j) or (j, i)
                pair_key = tuple(sorted([i, j]))

                # Check if pair already exists
                if pair_key in similarity_cache:
                    percentage_similarity = similarity_cache[pair_key]
                else:
                    # All possible aligments between 2 sequences
                    alignments = pairwise2.align.globalxx(target_seq, compare_seq)

                    # First is best because pairwise2 return sorted list by score
                    best_alignment = alignments[0]

                    # 0 and 1 are sequences and 2 is score
                    score = best_alignment[2] 

                    start_target = best_alignment[3]
                    end_target = best_alignment[4]

                    # Length of aligment
                    alignment_length = end_target - start_target

                    # Percentage similarity relative to the entire population
                    percentage_similarity = (score / alignment_length) * 100 if alignment_length > 0 else 0
                    similarity_cache[pair_key] = percentage_similarity

                total_similarity += percentage_similarity
                count += 1

        # Average similarity for given sequence
        average_similarity = total_similarity / count if count > 0 else 0
        global_similarities.append(average_similarity)
        target_obj.average_similarity = average_similarity

    # Izračun minimalnih i maksimalnih sličnosti
    min_sim = np.min(global_similarities)
    max_sim = np.max(global_similarities)
    
    # Izračun kazni
    penalties = calculate_penalty(global_similarities, min_sim, max_sim, penalty_function_reducer)

    # Primijeni kazne na populaciju
    for peptide, penalty in zip(population, penalties):
        # Primjeni kaznu na ff_amp_probability
        peptide.ff_amp_probability -= penalty
    
    # Pohrani vrijednosti za statistiku
    similarity_threshold_values.append(np.percentile(global_similarities, 67))
    similarity_min_values.append(min_sim)
    similarity_max_values.append(max_sim)
    similarity_mean_values.append(np.mean(global_similarities))
    
    return similarity_threshold_values, similarity_min_values, similarity_max_values, similarity_mean_values
