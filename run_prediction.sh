#!/bin/bash

cd /home/mataci/Desktop/seqprops_therapeutic
# Aktiviraj myenv2 environment
source /home/mataci/Desktop/seqprops_therapeutic/myenv2/bin/activate

# Pokreni prediction_script.py s proslijeđenim argumentima
python /home/mataci/Desktop/seqprops_therapeutic/prediction_script.py "$@"
