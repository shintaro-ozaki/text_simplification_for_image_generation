#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-nam=text-evaluate-clip-score-5
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

echo "pattern5"

echo "dreamlike-photoreal-2.0, LLama-3.1-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/dreamlike-photoreal-2.0/Llama-3.1-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "dreamlike-photoreal-2.0, LLama-3.1-8B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/dreamlike-photoreal-2.0/Llama-3.1-8B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "dreamlike-photoreal-2.0, LLama-3.3-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/dreamlike-photoreal-2.0/Llama-3.3-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "dreamlike-photoreal-2.0, Phi-3.5-mini-instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/dreamlike-photoreal-2.0/Phi-3.5-mini-instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "dreamlike-photoreal-2.0, Qwen2.5-72B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/dreamlike-photoreal-2.0/Qwen2.5-72B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, LLama-3.1-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/IF-I-L-v1.0/Llama-3.1-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, LLama-3.1-8B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/IF-I-L-v1.0/Llama-3.1-8B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, LLama-3.3-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/IF-I-L-v1.0/Llama-3.3-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, Phi-3.5-mini-instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/IF-I-L-v1.0/Phi-3.5-mini-instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "IF-I-L-v1.0, Qwen2.5-72B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/IF-I-L-v1.0/Qwen2.5-72B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "stable-diffusion-3.5-large, LLama-3.1-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/stable-diffusion-3.5-large/Llama-3.1-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "stable-diffusion-3.5-large, LLama-3.1-8B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/stable-diffusion-3.5-large/Llama-3.1-8B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "stable-diffusion-3.5-large, LLama-3.3-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/stable-diffusion-3.5-large/Llama-3.3-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "stable-diffusion-3.5-large, Phi-3.5-mini-instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/stable-diffusion-3.5-large/Phi-3.5-mini-instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "stable-diffusion-3.5-large, Qwen2.5-72B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/stable-diffusion-3.5-large/Qwen2.5-72B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "FLUX.1-dev, LLama-3.1-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/FLUX.1-dev/Llama-3.1-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "FLUX.1-dev, LLama-3.1-8B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/FLUX.1-dev/Llama-3.1-8B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "FLUX.1-dev, LLama-3.3-70B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/FLUX.1-dev/Llama-3.3-70B-Instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "FLUX.1-dev, Phi-3.5-mini-instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/FLUX.1-dev/Phi-3.5-mini-instruct.180.iterative3 data/reference_caption/
echo "##############"

echo "FLUX.1-dev, Qwen2.5-72B-Instruct.180.iterative3, pattern5"
python -m clip_score generated_images/pattern5/FLUX.1-dev/Qwen2.5-72B-Instruct.180.iterative3 data/reference_caption/
echo "##############"
