#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=openai
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

python $project/src/calculate.openai.price.py

echo "Done"
