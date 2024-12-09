#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:6000:1
#SBATCH --account=is-nlp
#SBATCH --job-name=make-prompt-qwen72b-77token
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

model=Qwen/Qwen2.5-72B-Instruct
quantize_type=4bit
batch_size=1
max_new_tokens=200

echo "Model: $model, Quantize: $quantize_type, Batch size: $batch_size, Max new tokens: $max_new_tokens"
time python $project/src/111224_add_summary_prompt.77token.py \
    --model $model \
    --quantize_type $quantize_type \
    --batch_size $batch_size \
    --max_new_tokens $max_new_tokens

echo "Done"
