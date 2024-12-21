#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=filter4
#SBATCH -o logs/slurm-%x-%j.log
set -eu

project=$(pwd)
source $project/.venv/bin/activate

# pattern3
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

# 全ての組み合わせを独立したジョブとして投げる
for diffusion_model in "${diffusion_models[@]}"; do
  for summarize_model in "${summarize_model[@]}"; do
    sbatch --export=ALL,diffusion_model="$diffusion_model",summarize_model="$summarize_model",project="$project" <<EOF
#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=filter4-${diffusion_model##*/}-${summarize_model##*/}
#SBATCH -o logs/slurm-%x-%j.log
set -eu

source \$project/.venv/bin/activate
python \$project/src/121524.remove.referene.invalid.file.py \
    --pattern 4 \
    --diffusion_model \$diffusion_model \
    --summarize_model \$summarize_model
EOF
  done
done
