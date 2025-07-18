# Evolution of antimicrobial peptides and modelling of the peptide template

##### Mateo Acinger

This repository contains Python scripts necessary to reproduce the results from the paper "Evolution of antimicrobial peptides and modelling of the peptide template." It also contains the results we obtained as well as instructions for performing additional analyses, visualizations.

---

## Steps to reproduce the results

### 1. Environment Setup

1. Clone this repository locally:  
   git clone https://github.com/MatAci/NSGA-II_antimicrobial_peptide_evolution.git

2. Once cloned, open the terminal and navigate to the root directory of the cloned repository.

3. Create a new virtual environment with Python 3.10.12 and install required packages from the requirements.txt

### 2. Terminal command

For Windows users:

	#Create a virtual environment  
	python3 -m venv env

	#Activate the virtual environment  
	env\Scripts\activate

	#Install the required packages  
	pip install -r requirements.txt

 For Linux users:

	# Create a virtual environment  
	python3 -m venv env

	# Activate the virtual environment  
	source env/bin/activate

	# Install the required packages  
	pip install -r requirements.txt

### 3. Clone repository with AMP model used in our algorithm
Clone this repository locally:  
git clone https://github.com/eotovic/seqprops_therapeutic.git

### 4. Set the paths

Set the root path of your locally cloned repository(https://github.com/eotovic/seqprops_therapeutic) inside the `run_predictions.sh` script.

---

## How to Run the Code
### Genetic Algorithm
1. Adjust input parameters:  
   Input configuration parameters can be adjusted directly inside main.py before execution (for reproduction of results leave it as they are now).

2. Run the genetic algorithm:  
   Execute the main.py script to start the genetic algorithm with a random initial population.  
   This script automatically runs the code located in the geneticAlgorithm folder.

3. Outputs:  
   The program will generate:  
   - A graph of the best Pareto front found.  
   - A convex hull curve.  
   - A graph showing the mean similarity of the population across generations.

4. Using the similarity array for comparisons:  
   The similarity values per generation are printed in the console as an array.  
   You can copy this array and use it in ploting/MultipleMeanPloting.py to visualize multiple algorithm runs simultaneously, comparing population similarity behavior across runs.

5. Accessing sequence and fitness outputs:  
   In the geneticAlgorithmOutputFiles folder, you will find results.txt, which contains:  
   - The character sequence (peptide string),  
   - Two fitness values (AMP probability and toxicity),  
   - The area under the convex hull curve.  
   By removing the header and convex hull area line from results.txt, you can paste the cleaned data into ploting/MultipleParetoFronts.py to graphically display multiple best Pareto fronts on the same plot for direct comparison.

---

### Analysis of pareto front

All of this code is in the analysis folder.
1. Copy results of Genetic algorithm
- Before running, copy the content of geneticAlgortihmOutputFiles/results.txt without the header and convex hull area into analysis/front.txt.

2. Find the most dominant point on the Pareto front
  - Run analysis/BestPointOfFront.py to find the point that is most dominant in both fitness functions (closest to the top-right corner of the graph).  

3. Convert Pareto front to FASTA format  
  - Use frontToFastaConverter.py to convert the Pareto front output from the genetic algorithm into a FASTA file used for MUSCLE alignment.

4. Run MUSCLE alignment  
   - Upload the generated analysis/fasta.txt to [MUSCLE](https://www.ebi.ac.uk/jdispatcher/msa/muscle?stype=protein&format=clwstrict).  
   - Choose ClustalW strict format and submit the job.  
   - When the job is finished, download the .fa file (The alignment in FASTA format converted by Seqret) from the result files.  
   - The alignment in FASTA format converted by Seqret should be copied into analysis/muscleOutput.txt.

5. Preparing alignment from MUSCLE output  
   - Once you have muscleOutput.txt, run MuscleOutputToMuscleAlignment.py to extract only the alignment.  
   - This script will generate analysis/muscleAlignment.txt containing just the alignment.

6. Creating sequence logo graph  
   - Upload analysis/muscleAlignment.txt to the [WebLogo website](https://weblogo.berkeley.edu/) as input.  
   - Set bits to 3 and create the sequence logo.

7. Subsequence counting analysis  
   - Run FastaAlignmentAnalysis.py using data from muscleOutput.txt.  
   - This script counts subsequences of lengths 2, 3, 4, and 5.  
   - Copy the output manually into the file resultsFromAnalysis.txt.  
   - If you have results from multiple runs, append them all into resultsFromAnalysis.txt.  
   - Separate results from different runs with a line containing --- to distinguish them for the next analysis script.

8. Frequency analysis of subsequences  
   - After filling resultsFromAnalysis.txt with correctly formatted data, run the script FrequencyOfSubSequences.py.  
   - This script generates the file resultsFromFrequency.txt.  
   - The output file contains counts of how many times each subsequence appeared in each run of the genetic algorithm.

After running all scripts in the analysis folder, you should have:  
- Sequence logo graphs,  
- Counts of subsequence attributes,  
- Frequency of attributes,  
- Correlations with other algorithm runs.

Based on these results, you can freely choose which attributes and subsequence lengths to focus on for further exploration.  
If you try to reproduce results go with HK, IYW and WHR.

---

### Subsequence Exploration

- Inside the subsequenceExploration folder, run the main program and inside main.py you can select the sequence you want to investigate.  
- For the chosen sequence, a population is generated using a sliding window approach.  
- The execution results show how each position affects antimicrobial peptide (AMP) activity and toxicity, whether thresholds are met, and how many of them.  
- You will also get visualization of threshold on the graph which you can save.  
- The population from each generation is saved in results.txt within the same folder.

---

### Template Algorithm

- If satisfied with how the attribute (sequence) performed relative to thresholds, you can create a template.  
- In the templateAlgorithm folder, run main.py and set the desired template with dashes (-) as the configurable parameter.  
- Running this program starts the genetic algorithm again, now optimizing only the unfixed regions of the template.  
- Outputs include:  
  - Graphical display of the Pareto front,  
  - Convex hull curve and area,  
  - Average similarity per generation.  
- Additionally, templateAlgorithm/results.txt contains the exact sequences for each generation and fitness values, also there are sequences in the best Pareto front.

---

### Template Shortening

- Navigate to the templateAllCombination folder.  
- Run the main.py script.  
- Set the configurable parameter as a template where variable parts are marked with -.  
- The script will generate all possible combinations for the variable parts.  
- The results, including the top 5 best sequences, are saved in templateAllCombination/results.txt.

---

With this, all the main steps are completed.
Feel free to contact me at acingermateo94@gmail.com
