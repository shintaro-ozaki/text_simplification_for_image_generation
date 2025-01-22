#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=eval-llama3.3
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

# fid
summarize_model=meta-llama/Llama-3.3-70B-Instruct

diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
  black-forest-labs/FLUX.1-dev
)

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 3"
  python $project/src/121724.evaluate.fid.py \
    --pattern 3 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1 &
  echo "Score appears to be calculated."
done

wait

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 4"
  python $project/src/121724.evaluate.fid.py \
    --pattern 4 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1 &
  echo "Score appears to be calculated."
done

wait

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 4"
  python $project/src/121724.evaluate.fid.py \
    --pattern 5 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1 &
  echo "Score appears to be calculated."
done

wait
