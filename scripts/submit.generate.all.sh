#!/bin/bash
#SBATCH -p lang_long
#SBATCH -c 2
#SBATCH -t 100:00:00
#SBATCH --account=lang
#SBATCH --job-name=submit

sbatch scripts/120924.deep.floyd.prompt.1.sh
sbatch scripts/120924.deep.floyd.prompt.2.sh

# sbatch scripts/120924.deep.floyd.prompt.3.llama8b.sh
sbatch scripts/120924.deep.floyd.prompt.3.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.3.3.3.llama70b.sh
sbatch scripts/120924.deep.floyd.prompt.3.phi.sh
sbatch scripts/120924.deep.floyd.prompt.3.qwen.sh
sbatch scripts/120924.deep.floyd.prompt.4.phi.sh
sbatch scripts/120924.deep.floyd.prompt.4.qwen.sh
# sbatch scripts/120924.deep.floyd.prompt.4.llama8b.sh
sbatch scripts/120924.deep.floyd.prompt.4.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.4.3.3.llama70b.sh
sbatch scripts/120924.deep.floyd.prompt.5.phi.sh
sbatch scripts/120924.deep.floyd.prompt.5.qwen.sh
# sbatch scripts/120924.deep.floyd.prompt.5.llama8b.sh
sbatch scripts/120924.deep.floyd.prompt.5.llama70b.sh
# sbatch scripts/120924.deep.floyd.prompt.5.3.3.llama70b.sh

sbatch scripts/120924.dreamlike.prompt.1.sh
sbatch scripts/120924.dreamlike.prompt.2.sh

sbatch scripts/120924.dreamlike.prompt.3.phi.sh
sbatch scripts/120924.dreamlike.prompt.3.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.3.llama8b.sh
sbatch scripts/120924.dreamlike.prompt.3.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.3.3.3.llama70b.sh
sbatch scripts/120924.dreamlike.prompt.4.phi.sh
sbatch scripts/120924.dreamlike.prompt.4.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.4.llama8b.sh
sbatch scripts/120924.dreamlike.prompt.4.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.4.3.3.llama70b.sh
sbatch scripts/120924.dreamlike.prompt.5.phi.sh
sbatch scripts/120924.dreamlike.prompt.5.qwen.sh
# sbatch scripts/120924.dreamlike.prompt.5.llama8b.sh
sbatch scripts/120924.dreamlike.prompt.5.llama70b.sh
# sbatch scripts/120924.dreamlike.prompt.5.3.3.llama70b.sh

sbatch scripts/120924.stable.diffusion.prompt.1.sh
sbatch scripts/120924.stable.diffusion.prompt.2.sh

sbatch scripts/120924.stable.diffusion.prompt.3.phi.sh
sbatch scripts/120924.stable.diffusion.prompt.3.qwen.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.llama8b.sh
sbatch scripts/120924.stable.diffusion.prompt.3.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.3.3.3.llama70b.sh
sbatch scripts/120924.stable.diffusion.prompt.4.phi.sh
sbatch scripts/120924.stable.diffusion.prompt.4.qwen.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.llama8b.sh
sbatch scripts/120924.stable.diffusion.prompt.4.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.4.3.3.llama70b.sh
sbatch scripts/120924.stable.diffusion.prompt.5.phi.sh
sbatch scripts/120924.stable.diffusion.prompt.5.qwen.sh
# sbatch scripts/120924.stable.diffusion.prompt.5.llama8b.sh
sbatch scripts/120924.stable.diffusion.prompt.5.llama70b.sh
# sbatch scripts/120924.stable.diffusion.prompt.5.3.3.llama70b.sh
