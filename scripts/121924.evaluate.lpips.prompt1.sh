#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=LPIPS-1
#SBATCH -o logs/slurm-%x-%j.log

set -eu

project=$(pwd)
source $project/.venv/bin/activate

# pattern1
pattern=pattern1

model_name=stable-diffusion-3.5-large
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/lpips.json

model_name=IF-I-L-v1.0
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/lpips.json

model_name=dreamlike-photoreal-2.0
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/lpips.json

model_name=FLUX.1-dev
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/lpips.json

echo "Done!"
