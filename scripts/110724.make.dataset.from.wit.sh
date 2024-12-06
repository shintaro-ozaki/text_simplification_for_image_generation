#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 8
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=wit
#SBATCH -o logs/slurm-%x-%j.log
#SBATCH --mail-type=END
#SBATCH --mail-user=slack:U06SLUE1DS8
set -eu

project=$(pwd)

source $project/.venv/bin/activate

python $project/src/110724_make_dataset_from_wit.py
echo "Done"
