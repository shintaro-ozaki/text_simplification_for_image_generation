#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:a6000:1
#SBATCH --account=is-nlp
#SBATCH --job-name=dreamlike-prompt3
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.dreamlike.prompt.3.4.py \
  --prompt 3 \
  --summarize_model microsoft/Phi-3.5-mini-instruct \
  --max_token 512

echo "Done"
