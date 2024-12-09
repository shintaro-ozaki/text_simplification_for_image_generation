#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:6000:1
#SBATCH --account=is-nlp
#SBATCH --job-name=sd3.5-prompt4
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

time python $project/src/120924.stable.diffusion.prompt.3.4.py \
    --prompt 4 \
    --summarize_model Qwen/Qwen2.5-72B \
    --max_token 70

echo "Done"
