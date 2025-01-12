#!/bin/bash
#SBATCH -p lang_gpu_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:a6000:1
#SBATCH --account=lang
#SBATCH --job-name=sd3.5-prompt4
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

<<_COMMENT_OUT
モデル
meta-llama/Llama-3.1-8B-Instruct
meta-llama/Llama-3.1-70B-Instruct
meta-llama/Llama-3.3-70B-Instruct
Qwen/Qwen2.5-72B
microsoft/Phi-3.5-mini-instruct
_COMMENT_OUT

time python $project/src/120924.stable.diffusion.prompt.3.4.py \
  --prompt 4 \
  --summarize_model Qwen/Qwen2.5-72B-Instruct \
  --max_token 180

echo "Done"
