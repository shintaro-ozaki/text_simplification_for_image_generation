sbatch scripts/111324.add.summary.prompt.77tokens.by.qwen72b.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.llama70b.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.3.3.llama70b.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.llama8b.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.phi.sh

exit 0

sbatch scripts/111224.add.summary.prompt.by.qwen72b.sh
sbatch scripts/111224.add.summary.prompt.by.llama70b.sh
sbatch scripts/111224.add.summary.prompt.by.phi.sh
sbatch scripts/111224.add.summary.prompt.by.llama8b.sh
sbatch scripts/111224.add.summary.prompt.by.3.3.llama70b.sh

sbatch scripts/111324.add.summary.prompt.77tokens.by.qwen72b.iterative.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.llama70b.iterative.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.phi.iterative.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.llama8b.iterative.sh
sbatch scripts/111324.add.summary.prompt.77tokens.by.3.3.llama70b.iterative.sh
