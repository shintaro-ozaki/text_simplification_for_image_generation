#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 8
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:1080:1
#SBATCH --account=is-nlp
#SBATCH --job-name=install
#SBATCH -o slurm-%x-%j.log

set -eu

project=$(pwd)

source $project/.venv/bin/activate
# uv pip install xformers
uv pip install pytorch-fid

echo "Installed all dependencies"
