#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=勤労
#SBATCH -o logs/slurm-%x-%j.log

set -eu


project=$(pwd)
source $project/.venv/bin/activate

python $project/src/120824_make_batch_data_for_openai.py
