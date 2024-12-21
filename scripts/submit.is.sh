#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=sample

sbatch scripts/121624.evaluate.inception.score-prompt1.sh
sbatch scripts/121624.evaluate.inception.score-prompt2.sh
sbatch scripts/121624.evaluate.inception.score-prompt3.sh
sbatch scripts/121624.evaluate.inception.score-prompt4.sh
sbatch scripts/121624.evaluate.inception.score-prompt5.sh
