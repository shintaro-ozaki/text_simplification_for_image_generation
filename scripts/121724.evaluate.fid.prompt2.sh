#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=FID-2
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

<<_COMMENT

画像の生成モデルには
- stabilityai/stable-diffusion-3.5-large
- DeepFloyd/IF-I-L-v1.0
- dreamlike-art/dreamlike-photoreal-2.0

要約モデルには
- meta-llama/Llama-3.3-70B-Instruct
- meta-llama/Llama-3.1-70B-Instruct
- meta-llama/Llama-3.1-8B-Instruct
- Qwen/Qwen2.5-72B-Instruct
- openai
- microsoft/Phi-3.5-mini-instruct
_COMMENT

# pattern2
diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
  black-forest-labs/FLUX.1-dev
)
# for-loop
for diffusion_model in ${diffusion_models[@]}; do
  python $project/src/121724.evaluate.fid.py \
    --pattern 2 \
    --diffusion_model $diffusion_model \
    --batch_size 1
  echo "Score appears to be calculated."
done
