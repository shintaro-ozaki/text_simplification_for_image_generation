#!/bin/bash
#SBATCH -p gpu_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --gres=gpu:3090:1
#SBATCH --account=is-nlp
#SBATCH --job-name=make-prompt
#SBATCH -o logs/slurm-%x-%j.log
#SBATCH --mail-type=END
#SBATCH --mail-user=slack:U06SLUE1DS8

project=$(pwd)
source $project/.venv/bin/activate

# time python $project/src/111224_add_summary_prompt_by_hf.py \
#     --model meta-llama/Llama-3.1-70B \
#     --quantize_type 4bit

model=microsoft/Phi-3.5-mini-instruct
quantize_type=none
batch_size=1
max_new_tokens=70

echo "Model: $model, Quantize: $quantize_type, Batch size: $batch_size, Max new tokens: $max_new_tokens"
time python $project/src/111224_add_summary_prompt_by_hf.py \
    --model $model \
    --quantize_type $quantize_type \
    --batch_size $batch_size \
    --max_new_tokens $max_new_tokens


echo "Done"
