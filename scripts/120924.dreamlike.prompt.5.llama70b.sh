#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:a100:1
#SBATCH --account=is-nlp
#SBATCH --job-name=dreamlike-prompt5
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.dreamlike.prompt.5.py \
  --prompt 5 \
  --summarize_model meta-llama/Llama-3.1-70B-Instruct \
  --max_token 180 \
  --iterative 3

echo "Done"
