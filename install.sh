#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 8
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=install
#SBATCH -o logs/slurm-%x-%j.log

set -eu

project=$(pwd)

source $project/.venv/bin/activate
# uv pip install xformers
# uv pip install pytorch-fid
# uv pip install git+https://github.com/openai/CLIP.git
uv pip install diffusers

echo "Installed all dependencies"
