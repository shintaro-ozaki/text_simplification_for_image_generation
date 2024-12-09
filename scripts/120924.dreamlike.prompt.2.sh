#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:a6000:1
#SBATCH --account=is-nlp
#SBATCH --job-name=dreamlike-prompt2
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.dreamlike.prompt.1.2.py \
    --prompt 2 \

echo "Done"
