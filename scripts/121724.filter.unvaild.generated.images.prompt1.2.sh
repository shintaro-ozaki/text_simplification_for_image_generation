#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=fiter_unvalid_generated_images-prompt1.2
#SBATCH -o logs/slurm-%x-%j.log

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

project=$(pwd)
source $project/.venv/bin/activate

# Pattern1
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern1/IF-I-L-v1.0 \
  --output_dir $project/filtered_generated_images/pattern1/IF-I-L-v1.0
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern1/dreamlike-photoreal-2.0 \
  --output_dir $project/filtered_generated_images/pattern1/dreamlike-photoreal-2.0
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern1/stable-diffusion-3.5-large \
  --output_dir $project/filtered_generated_images/pattern1/stable-diffusion-3.5-large
echo '============================================='

# Pattern2
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern2/IF-I-L-v1.0 \
  --output_dir $project/filtered_generated_images/pattern2/IF-I-L-v1.0
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern2/dreamlike-photoreal-2.0 \
  --output_dir $project/filtered_generated_images/pattern2/dreamlike-photoreal-2.0
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern2/stable-diffusion-3.5-large \
  --output_dir $project/filtered_generated_images/pattern2/stable-diffusion-3.5-large
echo '============================================='
