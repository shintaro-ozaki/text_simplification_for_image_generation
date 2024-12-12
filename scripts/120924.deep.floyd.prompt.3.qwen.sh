#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --account=is-nlp
#SBATCH --job-name=deep-floyd-prompt3
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.deep.floyd.prompt.3.4.py \
    --prompt 3 \
    --summarize_model Qwen/Qwen2.5-72B-Instruct \
    --max_token 512


echo "Done"
