#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=sample

sbatch scripts/121724.evaluate.fid.prompt1.sh
sbatch scripts/121724.evaluate.fid.prompt2.sh
sbatch scripts/121724.evaluate.fid.prompt3.sh
sbatch scripts/121724.evaluate.fid.prompt4.sh
sbatch scripts/121724.evaluate.fid.prompt5.sh
