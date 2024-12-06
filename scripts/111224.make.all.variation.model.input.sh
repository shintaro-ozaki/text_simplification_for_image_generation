#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=make-all-variation-model-input
#SBATCH -o logs/slurm-%x-%j.log

set -eu

project=$(pwd)
source $project/.venv/bin/activate

python $project/src/111224_make_all_variation_model_input.py

echo "Done"
