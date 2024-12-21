#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --account=is-nlp
#SBATCH --job-name=deep-floyd-prompt5
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.deep.floyd.prompt.5.py \
  --prompt 5 \
  --summarize_model meta-llama/Llama-3.3-70B-Instruct \
  --max_token 200 \
  --iterative 3

echo "Done"
