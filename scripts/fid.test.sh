#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=FID-test
#SBATCH -o logs/slurm-%x-%j.log

set -eu

# https://github.com/mseitzer/pytorch-fid

project=$(pwd)
source $project/.venv/bin/activate

time python -m pytorch_fid generated_images/pattern1/IF-I-L-v1.0/ wit_images_2k/
