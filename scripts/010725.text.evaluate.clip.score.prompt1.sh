#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=text-evaluate-clip-score-1
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

# pattern1
echo "pattern1"

echo "stable-diffusion-3.5-large, pattern1"
python -m clip_score generated_images/pattern1/stable-diffusion-3.5-large/ data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, pattern2"
python -m clip_score generated_images/pattern1/IF-I-L-v1.0 data/reference_caption/
echo "##############"

echo "dreamlike-photoreal-2.0, pattern1"
python -m clip_score generated_images/pattern1/dreamlike-photoreal-2.0 data/reference_caption/
echo "##############"

echo "flux-1.0.dev, pattern1"
python -m clip_score generated_images/pattern1/FLUX.1-dev data/reference_caption/
echo "##############"
