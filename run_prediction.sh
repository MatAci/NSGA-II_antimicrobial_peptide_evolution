#!/bin/bash

# Navigate to the local seqprops_therapeutic repository
cd /home/mataci/Desktop/seqprops_therapeutic

# Activate the myenv2 virtual environment
source /home/mataci/Desktop/seqprops_therapeutic/myenv2/bin/activate

# Run prediction_script.py with any passed arguments
python /home/mataci/Desktop/seqprops_therapeutic/prediction_script.py "$@"
