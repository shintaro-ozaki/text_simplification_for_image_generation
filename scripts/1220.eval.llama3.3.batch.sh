#!/bin/bash

# Set variables
project=$(pwd)
summarize_model=meta-llama/Llama-3.3-70B-Instruct
diffusion_models=(
  stabilityai/stable-diffusion-3.5-large
  DeepFloyd/IF-I-L-v1.0
  dreamlike-art/dreamlike-photoreal-2.0
  black-forest-labs/FLUX.1-dev
)

# Generate sbatch scripts dynamically
for pattern in 3 4 5; do
  for diffusion_model in "${diffusion_models[@]}"; do
    job_name="eval-pattern-${pattern}-$(basename $diffusion_model)"
    script="sbatch_scripts/${job_name}.sh"

    mkdir -p sbatch_scripts

    cat <<EOF > $script
#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 16
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=${job_name}
#SBATCH -o logs/slurm-%x-%j.log

source $project/.venv/bin/activate
echo "diffusion_model: $diffusion_model, summarize_model: $summarize_model, pattern: $pattern"
python $project/src/121724.evaluate.fid.py \\
  --pattern $pattern \\
  --diffusion_model $diffusion_model \\
  --summarize_model $summarize_model \\
  --batch_size 1
echo "Score appears to be calculated."
EOF

    # Submit the generated script
    sbatch $script
  done
done
