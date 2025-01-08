#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=eval-llama3.3
#SBATCH -o logs/slurm-%x-%j.log
set -eu

project=$(pwd)
source $project/.venv/bin/activate

# lpips
model_name=IF-I-L-v1.0
pattern=pattern3
summarize_model_name=Llama-3.3-70B-Instruct.512
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern4
summarize_model_name=Llama-3.3-70B-Instruct.200
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern5
summarize_model_name=Llama-3.3-70B-Instruct.200.iterative3
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

model_name=stable-diffusion-3.5-large
pattern=pattern3
summarize_model_name=Llama-3.3-70B-Instruct.512
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern4
summarize_model_name=Llama-3.3-70B-Instruct.200
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern5
summarize_model_name=Llama-3.3-70B-Instruct.200.iterative3
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

model_name=dreamlike-photoreal-2.0
pattern=pattern3
summarize_model_name=Llama-3.3-70B-Instruct.512
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern4
summarize_model_name=Llama-3.3-70B-Instruct.200
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern5
summarize_model_name=Llama-3.3-70B-Instruct.200.iterative3
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

model_name=FLUX.1-dev
pattern=pattern3
summarize_model_name=Llama-3.3-70B-Instruct.512
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern4
summarize_model_name=Llama-3.3-70B-Instruct.200
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json

pattern=pattern5
summarize_model_name=Llama-3.3-70B-Instruct.200.iterative3
reference_dir=$project/wit_images_2k/
generated_dir=$project/generated_images/$pattern/$model_name/$summarize_model_name/

python $project/src/121924.evaluate.lpips.py \
    -d0 $reference_dir \
    -d1 $generated_dir \
    -o $project/evaluated-lpips/$pattern/$model_name/$summarize_model_name/lpips.json


# is
diffusion_models=(
  # stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
)
summarize_model=meta-llama/Llama-3.3-70B-Instruct

for diffusion_model in ${diffusion_models[@]}; do
  for summarize_model in ${summarize_model[@]}; do
    echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 3"
    python $project/src/121624.evaluate.inception.score.py \
      --pattern 3 \
      --diffusion_model $diffusion_model \
      --summarize_model $summarize_model
  done
done

for diffusion_model in ${diffusion_models[@]}; do
  for summarize_model in ${summarize_model[@]}; do
    echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 3"
    python $project/src/121624.evaluate.inception.score.py \
      --pattern 4 \
      --diffusion_model $diffusion_model \
      --summarize_model $summarize_model
  done
done

for diffusion_model in ${diffusion_models[@]}; do
  for summarize_model in ${summarize_model[@]}; do
    echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 3"
    python $project/src/121624.evaluate.inception.score.py \
      --pattern 5 \
      --diffusion_model $diffusion_model \
      --summarize_model $summarize_model
  done
done

# fid
summarize_model=meta-llama/Llama-3.3-70B-Instruct

diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
  FLUX-ML/FLUX.1-dev
)

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 3"
  python $project/src/121724.evaluate.fid.py \
    --pattern 3 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1
  echo "Score appears to be calculated."
done

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 4"
  python $project/src/121724.evaluate.fid.py \
    --pattern 4 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1
  echo "Score appears to be calculated."
done

for diffusion_model in ${diffusion_models[@]}; do
  echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: 4"
  python $project/src/121724.evaluate.fid.py \
    --pattern 5 \
    --diffusion_model $diffusion_model \
    --summarize_model $summarize_model \
    --batch_size 1
  echo "Score appears to be calculated."
done
