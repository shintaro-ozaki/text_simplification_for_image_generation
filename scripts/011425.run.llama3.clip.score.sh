#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=llama3.3.clip.score
#SBATCH -o logs/slurm-%x-%j.log

echo 'Text CLIP score'
echo "FLUX.1-dev, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score generated_images/pattern4/FLUX.1-dev/Llama-3.3-70B-Instruct.180 data/reference_caption/
echo "##############"

echo 'Image CLIP score'
echo "FLUX.1-dev, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score wit_images_2k/ generated_images/pattern4/FLUX.1-dev/Llama-3.3-70B-Instruct.180 --real_flag img --fake_flag img
echo "##############"

