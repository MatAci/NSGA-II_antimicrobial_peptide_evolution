from Bio import pairwise2
import numpy as np


def applyPenaltyFactor(population,penalty_function_reducer):
    global_similarities = [] 
    
    for i, target_obj in enumerate(population):
        target_seq = target_obj.peptide_string
        total_similarity = 0
        count = 0
        
        for j, compare_obj in enumerate(population):
            if i != j:  
                compare_seq = compare_obj.peptide_string
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
                
                total_similarity += percentage_similarity
                count += 1
        
        # Average similarity for given sequence
        average_similarity = total_similarity / count if count > 0 else 0
        global_similarities.append(average_similarity)
        target_obj.average_similarity = average_similarity
    
    # We use 75% percentile beacuse it uses data instead of just positions
    threshold_percentile = np.percentile(global_similarities, 75)
    print(threshold_percentile)
    for peptide in population:
        if peptide.average_similarity > threshold_percentile:
            # Adjust the penalty factor as needed for positive values
            penalty = peptide.ff_amp_probability * penalty_function_reducer  
            peptide.ff_amp_probability -= penalty
          
            print(f"Sequence: {peptide.peptide_string}, Average Similarity Score: {peptide.average_similarity:.2f}% - Penalty")
        else:
            print(f"Sequence: {peptide.peptide_string}, Average Similarity Score: {peptide.average_similarity:.2f}% - No Penalty")