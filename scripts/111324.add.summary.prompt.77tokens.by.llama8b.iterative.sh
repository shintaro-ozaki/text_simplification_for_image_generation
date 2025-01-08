#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:a100:1
#SBATCH --account=is-nlp
#SBATCH --job-name=make-prompt-llama8b-1644
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

model=meta-llama/Llama-3.1-8B-Instruct
quantize_type=none
batch_size=1
max_new_tokens=180
iterative=3

echo "Model: $model, Quantize: $quantize_type, Batch size: $batch_size, Max new tokens: $max_new_tokens"
time python $project/src/111224_add_summary_prompt.77token.iterative.py \
  --model $model \
  --quantize_type $quantize_type \
  --batch_size $batch_size \
  --max_new_tokens $max_new_tokens \
  --iterative $iterative

echo "Done"
