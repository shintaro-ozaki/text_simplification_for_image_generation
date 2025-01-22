#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=evaluation
#SBATCH -o logs/slurm-%x-%j.log


echo '########## CLIP Score (text)##########'

echo "dreamlike-photoreal-2.0, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score generated_images/pattern4/dreamlike-photoreal-2.0/Llama-3.3-70B-Instruct.180 data/reference_caption/ & 
echo "##############"

echo "IF-I-L-v1.0, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score generated_images/pattern4/IF-I-L-v1.0/Llama-3.3-70B-Instruct.180 data/reference_caption/ & 
echo "##############"

echo "stable-diffusion-3.5-large, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score generated_images/pattern4/stable-diffusion-3.5-large/Llama-3.3-70B-Instruct.180 data/reference_caption/ & 
echo "##############"

echo "FLUX.1-dev, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score generated_images/pattern4/FLUX.1-dev/Llama-3.3-70B-Instruct.180 data/reference_caption/ & 
echo "##############"

wait

echo '########## CLIP Score (text) done ##########'

echo '########## CLIP Score (image) ##########'

echo "dreamlike-photoreal-2.0, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score wit_images_2k/ generated_images/pattern4/dreamlike-photoreal-2.0/Llama-3.3-70B-Instruct.180 --real_flag img --fake_flag img &
echo "##############"

echo "IF-I-L-v1.0, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score wit_images_2k/ generated_images/pattern4/IF-I-L-v1.0/Llama-3.3-70B-Instruct.180 --real_flag img --fake_flag img & 
echo "##############"

echo "stable-diffusion-3.5-large, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score wit_images_2k/ generated_images/pattern4/stable-diffusion-3.5-large/Llama-3.3-70B-Instruct.180 --real_flag img --fake_flag img & 
echo "##############"

echo "FLUX.1-dev, LLama-3.3-70B-Instruct.180, pattern4"
python -m clip_score wit_images_2k/ generated_images/pattern4/FLUX.1-dev/Llama-3.3-70B-Instruct.180 --real_flag img --fake_flag img & 
echo "##############"

echo '########## CLIP Score (image) done ##########'

echo "############### FID Score ###############"

diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
  black-forest-labs/FLUX.1-dev
)
summarize_model=meta-llama/Llama-3.3-70B-Instruct

for diffusion_model in ${diffusion_models[@]}; do
  python $project/src/121724.evaluate.fid.py \
    --pattern 4 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1 & 
  echo "Score appears to be calculated."
done

wait

echo "############### FID Score done ###############"

echo "############### IS Score ###############"

for diffusion_model in ${diffusion_models[@]}; do
  python $project/src/121624.evaluate.inception.score.py \
    --pattern 4 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model & 
  echo "Score appears to be calculated."
done

wait

echo "############### IS Score done ###############"

echo Done!
