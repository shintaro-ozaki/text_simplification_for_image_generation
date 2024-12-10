#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=download_wit_images
#SBATCH -o logs/slurm-%x-%j.log

project=$(pwd)
source $project/.venv/bin/activate

python $project/src/121024.wit.image.download.py

echo "Done"
