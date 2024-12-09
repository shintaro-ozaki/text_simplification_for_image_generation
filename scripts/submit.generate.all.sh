#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=submit


sbatch scripts/120924.deep.floyd.prompt.1.sh
sbatch scripts/120924.deep.floyd.prompt.2.sh
sbatch scripts/120924.deep.floyd.prompt.3.sh
sbatch scripts/120924.deep.floyd.prompt.4.sh

sbatch scripts/120924.dreamlike.prompt.1.sh
sbatch scripts/120924.dreamlike.prompt.2.sh
sbatch scripts/120924.dreamlike.prompt.3.sh
sbatch scripts/120924.dreamlike.prompt.4.sh

sbatch scripts/120924.stable.diffusion.prompt.1.sh
sbatch scripts/120924.stable.diffusion.prompt.2.sh
sbatch scripts/120924.stable.diffusion.prompt.3.sh
sbatch scripts/120924.stable.diffusion.prompt.4.sh
