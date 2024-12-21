#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --account=is-nlp
#SBATCH --job-name=deep-floyd-prompt4
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.deep.floyd.prompt.3.4.py \
  --prompt 4 \
  --summarize_model meta-llama/Llama-3.1-8B-Instruct \
  --max_token 200

echo "Done"
