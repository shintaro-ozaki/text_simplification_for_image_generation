#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 4
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=fiter_unvalid_generated_images-prompt3
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

# openai
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/openai.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/openai.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/openai.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/openai.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/openai.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/openai.512
echo '============================================='

# Pattern3
# meta-llama/Llama-3.3-70B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Llama-3.3-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Llama-3.3-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.3-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.3-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.3-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.3-70B-Instruct.512
echo '============================================='

# Pattern3
# meta-llama/Llama-3.3-70B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-70B-Instruct.512
echo '============================================='

# meta-llama/Llama-3.1-70B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-70B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-70B-Instruct.512
echo '============================================='

# meta-llama/Llama-3.1-8B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-8B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Llama-3.1-8B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-8B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Llama-3.1-8B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-8B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Llama-3.1-8B-Instruct.512
echo '============================================='

# Qwen/Qwen2.5-72B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Qwen-2.5-72B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Qwen-2.5-72B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Qwen-2.5-72B-Instruct.512
echo '============================================='

# Qwen/Qwen2.5-72B-Instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Qwen-2.5-72B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Qwen-2.5-72B-Instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Qwen-2.5-72B-Instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Qwen-2.5-72B-Instruct.512
echo '============================================='

# microsoft/Phi-3.5-mini-instruct
python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/IF-I-L-v1.0/Phi-3.5-mini-instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/IF-I-L-v1.0/Phi-3.5-mini-instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/dreamlike-photoreal-2.0/Phi-3.5-mini-instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/dreamlike-photoreal-2.0/Phi-3.5-mini-instruct.512
echo '============================================='

python $project/src/1217.filter.unvalid.generated.images.py \
  --input_dir $project/generated_images/pattern3/stable-diffusion-3.5-large/Phi-3.5-mini-instruct.512 \
  --output_dir $project/filtered_generated_images/pattern3/stable-diffusion-3.5-large/Phi-3.5-mini-instruct.512
echo '============================================='
