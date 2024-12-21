#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=evaluate-clip-score-1
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

# pattern1
echo "pattern1"

echo "stable-diffusion-3.5-large, pattern1"
python -m clip_score wit_images_2k/ generated_images/pattern1/stable-diffusion-3.5-large/ --real_flag img --fake_flag img
echo "##############"

echo "IF-I-L-v1.0, pattern2"
python -m clip_score wit_images_2k/ generated_images/pattern1/IF-I-L-v1.0 --real_flag img --fake_flag img
echo "##############"

echo "dreamlike-photoreal-2.0, pattern1"
python -m clip_score wit_images_2k/ generated_images/pattern1/dreamlike-photoreal-2.0 --real_flag img --fake_flag img
echo "##############"
