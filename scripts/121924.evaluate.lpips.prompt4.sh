#!/bin/bash
#SBATCH -p lang_mem_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=LPIPS-4
#SBATCH -o logs/slurm-%x-%j.log

set -eu

project=$(pwd)
source $project/.venv/bin/activate

<<COMMENT
Llama-3.1-8B-Instruct.180
Llama-3.3-70B-Instruct.180
Llama-3.1-70B-Instruct.180
Qwen2.5-72B-Instruct.180
Phi-3.5-mini-instruct.180
COMMENT

# pattern1
pattern=pattern4

model_name=stable-diffusion-3.5-large
summarize_model_name=Llama-3.1-8B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

echo "model_name: $model_name, summarize_model_name: $summarize_model_name, reference_dir: $reference_dir, generated_dir: $generated_dir, pattern: $pattern"

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.3-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

echo ###################################################################################################

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.1-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Qwen2.5-72B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Phi-3.5-mini-instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

########################################
model_name=IF-I-L-v1.0
summarize_model_name=Llama-3.1-8B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.3-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.1-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Qwen2.5-72B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Phi-3.5-mini-instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

################################################

model_name=dreamlike-photoreal-2.0
summarize_model_name=Llama-3.1-8B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.3-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.1-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Qwen2.5-72B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Phi-3.5-mini-instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

################################################

model_name=FLUX.1-dev
summarize_model_name=Llama-3.1-8B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.3-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Llama-3.1-70B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=openai.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Qwen2.5-72B-Instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

summarize_model_name=Phi-3.5-mini-instruct.180
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
  -d0 $reference_dir \
  -d1 $generated_dir \
  -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json



echo "Done!"
