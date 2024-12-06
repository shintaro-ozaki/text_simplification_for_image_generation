#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=split-wit
#SBATCH -o logs/slurm-%x-%j.log

set -eu

project=$(pwd)
source $project/.venv/bin/activate

python $project/src/110724_split_partial_data_from_raw_wit.py

echo "Done"
