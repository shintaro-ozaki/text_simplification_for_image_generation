#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=IS-4
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
- meta-llama/Llama-3.3-8B-Instruct
- Qwen/Qwen2.5-72B-Instruct
- openai
- microsoft/Phi-3.5-mini-instruct
_COMMENT

# pattern4
diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
)
summarize_model=(
  meta-llama/Llama-3.3-70B-Instruct
  meta-llama/Llama-3.1-70B-Instruct
  meta-llama/Llama-3.1-8B-Instruct
  Qwen/Qwen2.5-72B-Instruct
  microsoft/Phi-3.5-mini-instruct
)
# for-loop
for diffusion_model in ${diffusion_models[@]}; do
  for summarize_model in ${summarize_model[@]}; do
    echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 4"
    python $project/src/121624.evaluate.inception.score.py \
      --pattern 4 \
      --diffusion_model $diffusion_model \
      --summarize_model $summarize_model
  done
done
